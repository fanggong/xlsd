from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from services.sync_service import SyncService
from models.ods_cps_order import OdsCpsOrder
from database.mysql import db_session

import time
import logging

logger = logging.getLogger(__name__)

def sync_ods_cps_order():
    end_time = datetime.now()
    begin_time = datetime.now() - timedelta(seconds=12)
    open_id_lst = ['f18d5ec29982990414bf57246fc349dd', 'f18d5ec29982990414bf57243e2ae80e']

    # 定义时间分段的数量
    num_time_segments = 4
    time_segments = [(begin_time + (end_time - begin_time) * i / num_time_segments,
                     begin_time + (end_time - begin_time) * (i + 1) / num_time_segments)
                    for i in range(num_time_segments)]

    syns_service = SyncService(session=db_session)

    def process_segment(open_id, segment_begin_time, segment_end_time):
        logger.info(f'Processing open_id {open_id} from {segment_begin_time} to {segment_end_time}')
        syns_service.update_table(OdsCpsOrder, OdsCpsOrder.update_strategy,
                                  init_fetcher={'session': db_session},
                                  open_id=open_id, begin_time=segment_begin_time, end_time=segment_end_time)

    with ThreadPoolExecutor() as executor:
        futures = []
        for open_id in open_id_lst:
            for segment_begin_time, segment_end_time in time_segments:
                futures.append(executor.submit(process_segment, open_id, segment_begin_time, segment_end_time))

        # 等待所有任务完成
        for future in futures:
            future.result()