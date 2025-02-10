from ks.ksClient import KsClient
from . import const as c

from datetime import datetime

class OrdersApi(KsClient):
    def __init__(self, session, app_key, app_secret, sign_secret, sign_method, version=c.VERSION, base_url=c.BASE_URL, proxy=None):
        super().__init__(session, app_key, app_secret, sign_secret, sign_method, version, base_url, proxy=proxy)

    def get_cps_order(self, open_id: str, begin_time: datetime, end_time: datetime, cps_order_status: int = 0, 
                      sort_type: int = 2, query_type: int = 2, page_size: int = 100, pcursor: str = ''):
        begin_time = int(begin_time.timestamp() * 1000)
        end_time = int(end_time.timestamp() * 1000)
        access_token = self.get_access_token(open_id=open_id)
        params = {
            'sortType': sort_type,
            'queryType': query_type,
            'beginTime': begin_time,
            'endTime': end_time,
            'cpsOrderStatus': cps_order_status,
            'pageSize': page_size,
            'pcursor': pcursor
        }
        return self._request(c.GET, c.CPS_ORDER, access_token, params)

        # result = []
        # while params['pcursor'] != 'nomore':
        #     response = self._request(
        #         method=c.GET, access_token=access_token, api_name=c.CPS_ORDER, params=params
        #     )
        #     if response['msg'] == 'success':
        #         result = result + response['data']['orderView']
        #         params['pcursor'] = response['data']['pcursor']
        #         continue
        #     else:
        #         break

        # return result