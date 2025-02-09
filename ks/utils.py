from services.query_service import QueryService
from . import const as c

import time
import logging
import datetime

logger = logging.getLogger(__name__)


def get_tokens(session, open_id):
    retry_times = 0
    while retry_times < c.MAX_RETRY:
        try:
            res = QueryService.fetch_df_dat(
                session=session,
                sql=f'''
                select access_token, refresh_token, updated_at
                from xlsd.ks_token
                where open_id = '{open_id}'
                '''
            )
            break
        except BaseException as e:
            logger.info(str(e))
            retry_times = retry_times + 1
            logger.info(f'RETRYING {retry_times} TIMES...')
            time.sleep(3)

    return res['updated_at'][0], res['access_token'][0], res['refresh_token'][0]


def update_refresh_token(session, open_id, refresh_token, access_token):
    retry_times = 0
    while retry_times < c.MAX_RETRY:
        try:
            nowtime = datetime.now()
            QueryService.execute_raw_sql(
                session=session,
                sql=f'''
                update xlsd.ks_token
                set access_token = '{access_token}', refresh_token = '{refresh_token}',  updated_at = '{nowtime}'
                where open_id = '{open_id}'
                '''
            )
            break
        except BaseException as e:
            logger.info(e)
            retry_times = retry_times + 1
            logger.info(f'RETRYING {retry_times} TIMES...')
            time.sleep(3)

def timestamp_now():
    return int(datetime.now().timestamp() * 1000)
