from datetime import datetime, timedelta
from services.ods_cps_order_fetcher import OdsCpsOrderFetcher
from services.sync_service import SyncService
from models.ods_cps_order import OdsCpsOrder
from database.mysql import db_session

import time
import logging

logger = logging.getLogger(__name__)

def sync_ods_cps_order():
    session = db_session
    end_time = datetime.now()
    begin_time = datetime.now() - timedelta(seconds=12)
    open_id_lst = ['f18d5ec29982990414bf57246fc349dd', 'f18d5ec29982990414bf57243e2ae80e']

    odo_fetcher_api = OdsCpsOrderFetcher(session=session)
    syns_service = SyncService(session=session)

    for open_id in open_id_lst:
        logger.info(f'process for open_id {open_id}')
        syns_service.update_table(OdsCpsOrder, OdsCpsOrder.update_strategy)