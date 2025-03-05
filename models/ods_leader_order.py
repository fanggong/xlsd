from sqlalchemy import Column, String, Float, DECIMAL, BigInteger, TIMESTAMP
from database.mysql import Base
from services.update_strategy import UpdateStrategy


class OdsLeaderOrder(Base):
    __tablename__ = 'ods_leader_order'
    
    kwaimoney_user_nickname = Column(String(100))
    regimental_promotion_rate = Column(Float)
    pay_time = Column(TIMESTAMP)
    o_id = Column(String(100), primary_key=True)
    expend_estimate_settle_amount = Column(DECIMAL(20, 2))
    promotion_id = Column(String(100))
    expend_regimental_settle_amount = Column(DECIMAL(20, 2))
    activity_id = Column(String(100))
    pay_amount = Column(DECIMAL(20, 2))
    order_trade_amount = Column(DECIMAL(20, 2))
    settlement_success_time = Column(TIMESTAMP)
    expend_regimental_promotion_rate = Column(Float)
    activity_user_id = Column(String(100))
    promotion_type = Column(BigInteger)
    recv_time = Column(TIMESTAMP)
    share_rate_str = Column(Float)
    buyer_open_id = Column(String(100))
    order_create_time = Column(TIMESTAMP)
    promotion_nickname = Column(String(500))
    update_time = Column(TIMESTAMP, index=True)
    cps_order_status = Column(BigInteger)
    base_amount = Column(DECIMAL(20, 2))
    promotion_kwai_id = Column(String(100))
    send_time = Column(TIMESTAMP)
    create_time = Column(TIMESTAMP)
    send_status = Column(BigInteger)
    excitation_income = Column(DECIMAL(20, 2))
    kwaimoney_user_id = Column(String(100))
    settlement_amount = Column(DECIMAL(20, 2))
    item_id = Column(String(100))
    item_title = Column(String(100))
    item_price = Column(DECIMAL(20, 2))
    item_url = Column(String(550))
    seller_id = Column(String(100))
    seller_nickname = Column(String(100))
    sku_id = Column(String(100))
    regimental_promotion_amount = Column(DECIMAL(20, 2))
    fund_type = Column(BigInteger)
    settlement_biz_type = Column(BigInteger)
    service_income = Column(DECIMAL(20, 2))

    update_strategy = UpdateStrategy.INCREMENTAL

    def __repr__(self):
        return f'<OdsLeaderOrder(o_id="{self.o_id}, order_create_time="{self.order_create_time}", promotion_id="{self.promotion_id}")>'