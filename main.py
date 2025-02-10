from services.query_service import QueryService
from database.mysql import db_session
from ks.ksClient import KsClient
from ks.Orders import OrdersApi
from config import Config
from datetime import datetime
from services.ods_cps_order_fetcher import OdsCpsOrderFetcher

import logging


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    cfg = Config.get_ks_cfg()
    oco_api = OdsCpsOrderFetcher(session=db_session())
    open_id='f18d5ec29982990414bf57246fc349dd'
    begin_time = datetime(2025, 1, 28, 4, 0, 0)
    end_time = datetime(2025, 1, 28, 6, 0, 0)
    res = oco_api.fetch_data(open_id=open_id, begin_time=begin_time, end_time=end_time)
    print(len(res))
    # sql = '''
    # update xlsd.ks_token
    # set access_token = '1', refresh_token = '2',  updated_at = '2025-02-10 14:33:17.420559'
    # where open_id = 'f18d5ec29982990414bf5724eb5e7990'    
    # '''
    # tmp = QueryService.execute_raw_sql(db_session, 'select * from xlsd.ks_token')
    # print(tmp)