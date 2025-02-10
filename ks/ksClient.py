from httpx import Client
from datetime import datetime
from services.query_service import QueryService
from . import const as c
from . import utils as u


import urllib.parse
import logging
import json
import hmac
import hashlib
import base64
import time

logger = logging.getLogger(__name__)


class KsClient(Client):
    def __init__(self, session, app_key, app_secret, sign_secret, sign_method, version=c.VERSION, base_url=c.BASE_URL, proxy=None):
        super().__init__(base_url=base_url, http2=True, proxy=proxy)
        self.session = session
        self.app_key = app_key
        self.app_secret = app_secret
        self.sign_secret = sign_secret
        self.sign_method = sign_method
        self.version = version
    
    def get_tokens(self, open_id):
        res = QueryService.fetch_df_dat(
            session=self.session,
            sql=f'''
            select access_token, refresh_token, updated_at
            from {c.TOKEN_TABLE}
            where open_id = '{open_id}'
            '''
        )
        return res['updated_at'][0], res['access_token'][0], res['refresh_token'][0]

    def update_refresh_token(self, open_id, refresh_token, access_token):
        nowtime = datetime.now()
        QueryService.execute_raw_sql(
            session=self.session,
            sql=f'''
            update {c.TOKEN_TABLE}
            set access_token = '{access_token}', refresh_token = '{refresh_token}', updated_at = '{nowtime}'
            where open_id = '{open_id}'
            '''
        )
        
    def generate_signature(self, params, access_token, api_name, timestamp):
        sign_string = {
            'access_token': access_token,
            'appkey': self.app_key,
            'method': api_name,
            'param': json.dumps(params),
            'signMethod': self.sign_method,
            'timestamp': timestamp,
            'version': self.version,
            'signSecret': self.sign_secret
        }
        sign_string = [f'{key}={value}' for key, value in sign_string.items() if value != 'null']
        sign_string = '&'.join(sign_string)
        signature = hmac.new(self.sign_secret.encode(), sign_string.encode(), hashlib.sha256).digest()
        signature = base64.b64encode(signature).decode()
        return signature
    
    
    def get_access_token(self, open_id: str):
        update_at, access_token, refresh_token = self.get_tokens(open_id=open_id)
        if (datetime.now() - update_at).total_seconds() / 3600 >= 24:
            logger.info(f'token expired. update tokens for {open_id}')
            url = 'https://openapi.kwaixiaodian.com/oauth2/refresh_token'
            body = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'app_id': self.app_key,
                'app_secret': self.app_secret
            }
            response = self.post(url, data=body).json()

            if response['result'] == 1:
                new_refresh_token = response['refresh_token']
                new_access_token = response['access_token']
                logger.info(f'new token get daze. access_token: {new_access_token}, refresh_token: {new_refresh_token}')

                self.update_refresh_token(
                    open_id=open_id,
                    access_token=new_access_token,
                    refresh_token=new_refresh_token
                )
                return new_access_token
            else:
                logger.info('tokens invalid')
                return c.TOKEN_ERROR_MSG
        return access_token
    
    def _request(self, method, api_name, access_token, params=None):
        timestamp = u.timestamp_now()
        signature = self.generate_signature(params=params, access_token=access_token, api_name=api_name, timestamp=timestamp)
        sys_params = urllib.parse.urlencode({
            'appkey': self.app_key,
            'timestamp': timestamp,
            'access_token': access_token,
            'version': self.version,
            'method': api_name,
            'sign': signature,
            'signMethod': self.sign_method
        })
        request_path = api_name + f'?{sys_params}'
        
        if method == c.GET:
            if params:
                code_params = urllib.parse.quote_plus(json.dumps(params))
                request_path = request_path + f'&param={code_params}'
            response = self.get(request_path)
        elif method == c.POST:
            response = self.post(request_path, data=json.dumps(params))
        else:
            raise ValueError('method must be GET or POST')

        # 错误处理
        # if response['code'] != '1':
        #     self.log_api(
        #         api_name=api_name,
        #         params=json.dumps(params),
        #         remark=json.dumps(response, ensure_ascii=False),
        #         access_token=access_token
        #     )

        # if response['code'] == '802000' and response['sub_code'] == '802005':
        #     time.sleep(10)
        #     raise BaseException('限流')
        # if response['code'] == '806000' and response['sub_code'] == '806001':
        #     time.sleep(5)
        #     raise BaseException('内部调用超时')

        return response.json()


