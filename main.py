from services.query_service import QueryService
from database.mysql import db_session
from ks.ksClient import KsClient
from config import Config
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    cfg = Config.get_ks_cfg()
    ksc = KsClient(
        app_key=cfg['app_key'], app_secret=cfg['app_secret'], sign_method=cfg['sign_method'], sign_secret=cfg['sign_secret']
    )
    res = ksc.get_access_token(session=db_session(), open_id='f18d5ec29982990414bf5724945e9124')
    print(res)