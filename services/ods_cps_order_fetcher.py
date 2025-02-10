from services.data_fetcher import DataFetcher
from ks.Orders import OrdersApi
from config import Config
from . import utils as u

import pandas as pd
import logging 

logger = logging.getLogger(__name__)


class OdsCpsOrderFetcher(DataFetcher):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def fetch_data(self, **kwargs):
        logger.info(f'{kwargs} SERVICE IS RUNING...')
        order_api = OrdersApi(session=self.session, **Config.get_ks_cfg())

        dat = []
        kwargs.setdefault('pcursor', '')

        while kwargs['pcursor'] != 'nomore':
            response = order_api.get_cps_order(**kwargs)
            if response['msg'] == 'success':
                dat = dat + response['data']['orderView']
                kwargs['pcursor'] = response['data']['pcursor']
                continue
            else:
                break
        dat = self.process_data(dat)
        return dat

    def process_data(self, dat):
        if len(dat) == 0:
            return None
        dat = [
            {
                'update_time': u.timestamp2datetime(each.get('updateTime')),
                'anchor_id': each.get('distributorId'),
                'order_create_time': u.timestamp2datetime(each.get('orderCreateTime')),
                'o_id': str(each.get('oid')),
                'item_id': each.get('cpsOrderProductView')[0].get('itemId') if each.get('cpsOrderProductView') else None,
                'item_title': each.get('cpsOrderProductView')[0].get('itemTitle') if each.get('cpsOrderProductView') else None,
                'order_trade_amount': each.get('orderTradeAmount'),
                'recv_time': u.timestamp2datetime(each.get('recvTime')),
                # 'share_rate_str': each.get('shareRateStr'),
                'share_rate_str': 900,
                'buyer_open_id': each.get('buyerOpenId'),
                'pay_time': u.timestamp2datetime(each.get('payTime')),
                'cps_order_status': each.get('cpsOrderStatus'),
                'base_amount': each.get('baseAmount'),
                'send_time': u.timestamp2datetime(each.get('sendTime')),
                'settlement_biz_type': each.get('settlementBizType'),
                'create_time': u.timestamp2datetime(each.get('createTime')),
                'settlement_success_time': u.timestamp2datetime(each.get('settlementSuccessTime')),
                'send_status': each.get('sendStatus'),
                'settlement_amount': each.get('settlementAmount'),
                'service_income': each.get('cpsOrderProductView')[0].get('serviceInCome') if each.get('cpsOrderProductView') else None,
                'commission_rate': each.get('cpsOrderProductView')[0].get('commissionRate') if each.get('cpsOrderProductView') else None,
                'cps_type': each.get('cpsOrderProductView')[0].get('cpsType') if each.get('cpsOrderProductView') else None,
                'num': each.get('cpsOrderProductView')[0].get('num') if each.get('cpsOrderProductView') else None,
                'step_commission_amount': each.get('cpsOrderProductView')[0].get('stepCommissionAmount') if each.get('cpsOrderProductView') else None,
                'cps_pid': each.get('cpsOrderProductView')[0].get('cpsPid') if each.get('cpsOrderProductView') else None,
                'step_commission_rate': each.get('cpsOrderProductView')[0].get('stepCommissionRate') if each.get('cpsOrderProductView') else None,
                'service_amount': each.get('cpsOrderProductView')[0].get('serviceAmount') if each.get('cpsOrderProductView') else None,
                'seller_id': each.get('cpsOrderProductView')[0].get('sellerId') if each.get('cpsOrderProductView') else None,
                'remise_commission_rate': each.get('cpsOrderProductView')[0].get('remiseCommissionRate') if each.get('cpsOrderProductView') else None,
                'seller_nick_name': each.get('cpsOrderProductView')[0].get('sellerNickName') if each.get('cpsOrderProductView') else None,
                'remise_commission_amount': each.get('cpsOrderProductView')[0].get('remiseCommissionAmount') if each.get('cpsOrderProductView') else None,
                'item_price': each.get('cpsOrderProductView')[0].get('itemPrice') if each.get('cpsOrderProductView') else None,
                'excitation_income': each.get('cpsOrderProductView')[0].get('excitationInCome') if each.get('cpsOrderProductView') else None,
                'service_rate': each.get('cpsOrderProductView')[0].get('serviceRate') if each.get('cpsOrderProductView') else None,
                'kwaimoney_user_id': each.get('cpsOrderProductView')[0].get('kwaimoneyUserId') if each.get('cpsOrderProductView') else None,
                'estimated_income': each.get('cpsOrderProductView')[0].get('estimatedIncome') if each.get('cpsOrderProductView') else None,
                'step_condition': each.get('cpsOrderProductView')[0].get('stepCondition') if each.get('cpsOrderProductView') else None
            }
            for each in dat
        ]
        return dat