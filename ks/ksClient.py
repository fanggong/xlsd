from httpx import Client
from datetime import datetime
from . import const as c
from . import utils as u

import urllib.parse
import logging
import json
import hmac
import hashlib
import base64
import requests
import time

logger = logging.getLogger(__name__)


class KsClient(Client):
    def __init__(self, app_key, app_secret, sign_secret, sign_method, version=c.VERSION, base_url=c.BASE_URL, proxy=None):
        super().__init__(base_url=base_url, http2=True, proxy=proxy)
        self.app_key = app_key
        self.app_secret = app_secret
        self.sign_secret = sign_secret
        self.sign_method = sign_method
        self.version = version

    def generate_signature(self, params, access_token, api_name, timestamp):
        # 构造签名字符串
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

        # 使用HMAC_SHA256算法生成签名
        signature = hmac.new(self.sign_secret.encode(), sign_string.encode(), hashlib.sha256).digest()
        signature = base64.b64encode(signature).decode()
        return signature
    
    
    def get_access_token(self, session, open_id: str):
        update_at, access_token, refresh_token = u.get_tokens(session=session, open_id=open_id)
        if (datetime.now() - update_at).total_seconds() / 3600 >= 24:
            logger.info(f'token expired. update tokens for {open_id}')

            retry_times = 0
            while retry_times < c.MAX_RETRY:
                try:
                    url = 'https://openapi.kwaixiaodian.com/oauth2/refresh_token'
                    body = {
                        'grant_type': 'refresh_token',
                        'refresh_token': refresh_token,
                        'app_id': self.app_key,
                        'app_secret': self.app_secret
                    }
                    response = requests.post(url, data=body).json()

                    if response['result'] == 1:
                        new_refresh_token = response['refresh_token']
                        new_access_token = response['access_token']
                        logger.info(f'new token get daze. access_token: {new_access_token}, refresh_token: {new_refresh_token}')

                        u.update_refresh_token(
                            session=session, 
                            open_id=open_id,
                            access_token=new_access_token,
                            refresh_token=new_refresh_token
                        )
                        return new_access_token
                    else:
                        logger.info('tokens invalid')
                        return c.TOKEN_ERROR_MSG

                except BaseException as e:
                    logger.info(str(e))
                    retry_times = retry_times + 1
                    logger.info(f'get new tokens retrying {retry_times} times...')
                    time.sleep(3)

            if retry_times == c.MAX_RETRY:
                return c.TOKEN_ERROR_MSG

        return access_token
    

    def request(self, method, api_name, access_token, params=None):
        timestamp = u.timestamp_now()
        signature = self.generate_signature(
            params=params, access_token=access_token, api_name=api_name, timestamp=timestamp
        )

        request_path = self.base_url + api_name.replace('.', '/')

        sys_params = urllib.parse.urlencode({
            'appkey': self.app_key,
            'timestamp': timestamp,
            'access_token': access_token,
            'version': self.version,
            'method': api_name,
            'sign': signature,
            'signMethod': self.sign_method
        })

        retry_time = 0
        remark = ''
        while retry_time < c.MAX_RETRY:
            try:
                # request
                url = f'{request_path}?{sys_params}'
                if method == 'GET':
                    if params:
                        code_params = urllib.parse.quote_plus(json.dumps(params))
                        url = url + f'&param={code_params}'
                    response = requests.get(url).json()
                elif method == 'POST':
                    response = requests.post(url, data=params).json()
                else:
                    raise ValueError('method must be GET or POST')
                logger.info(url)

                # 错误处理
                if response['code'] != '1':
                    self.log_api(
                        api_name=api_name,
                        params=json.dumps(params),
                        remark=json.dumps(response, ensure_ascii=False),
                        access_token=access_token
                    )

                if response['code'] == '802000' and response['sub_code'] == '802005':
                    time.sleep(10)
                    raise BaseException('限流')
                if response['code'] == '806000' and response['sub_code'] == '806001':
                    time.sleep(5)
                    raise BaseException('内部调用超时')

                return response

            except BaseException as e:
                remark = str(retry_time) + str(e)
                retry_time = retry_time + 1
                time.sleep(3)

        if retry_time == c.MAX_RETRY:
            self.log_api(api_name=api_name, params=json.dumps(params), remark=remark, access_token=access_token)

        return None

