from httpx import Client
from . import const as c

import logging
import json
import hmac
import hashlib
import base64

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