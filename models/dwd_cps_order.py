from sqlalchemy import Column, DECIMAL, String, DateTime, BigInteger, Float
from database.mysql import Base
from services.update_strategy import UpdateStrategy

class DwdCpsOrder(Base):
    __tablename__ = 'dwd_cps_order'

    update_time = Column(DateTime, nullable=True, comment='更新时间')
    anchor_id = Column(String(100), nullable=False, comment='分销推广者用户ID')
    order_create_time = Column(DateTime, nullable=True, comment='订单创建时间')
    o_id = Column(String(100), primary_key=True, nullable=False, comment='订单ID')
    item_id = Column(String(100), nullable=False, comment='商品ID')
    item_title = Column(String(100), nullable=False, comment='商品标题')
    order_trade_amount = Column(DECIMAL(10, 2), nullable=False, comment='订单交易总金额(/100)')
    recv_time = Column(DateTime, nullable=True, comment='订单收货时间')
    share_rate_str = Column(Float, nullable=True, comment='分成比例（千分比），100->10%,如果该返回值为“计算中”，请等待服务器计算完成，重新请求')
    buyer_open_id = Column(String(100), nullable=True, comment='买家唯一识别ID')
    pay_time = Column(DateTime, nullable=True, comment='订单支付时间')
    cps_order_status = Column(BigInteger, nullable=True, comment='分销订单状态 [0:全部订单] [30:已付款] [50:已收货] [60:已结算] [80:已失效]')
    base_amount = Column(DECIMAL(10, 2), nullable=True, comment='计佣基数（分）')
    send_time = Column(DateTime, nullable=True, comment='订单发货时间')
    settlement_biz_type = Column(BigInteger, nullable=True, comment='订单业务结算类型 1-快分销，2-聚力计划')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    settlement_success_time = Column(DateTime, nullable=True, comment='结算时间')
    send_status = Column(BigInteger, nullable=True, comment='订单发货状态（0:未发货，1:已发货）')
    settlement_amount = Column(DECIMAL(10, 2), nullable=True, comment='结算金额（分）')
    service_income = Column(DECIMAL(10, 2), nullable=True, comment='接单服务收入（分）')
    commission_rate = Column(Float, nullable=True, comment='佣金比率(千分比)')
    cps_type = Column(BigInteger, nullable=True)
    num = Column(BigInteger, nullable=False, comment='商品数量')
    step_commission_amount = Column(DECIMAL(10, 2), nullable=True, comment='阶梯佣金金额，达到阶梯条件并完成结算后，阶梯佣金金额（分），无阶梯条件或未结算完成为0')
    cps_pid = Column(String(100), nullable=True, comment='推广位id')
    step_commission_rate = Column(Float, nullable=True, comment='阶梯佣金比率，达到阶梯条件以后的佣金比率（千分比），没有阶梯条件则为0')
    service_amount = Column(DECIMAL(10, 2), nullable=True, comment='接单服务收入（分）')
    seller_id = Column(String(100), nullable=True, comment='商家Id')
    remise_commission_rate = Column(Float, nullable=True)
    seller_nick_name = Column(String(100), nullable=True, comment='商家昵称快照')
    remise_commission_amount = Column(DECIMAL(10, 2), nullable=True)
    item_price = Column(DECIMAL(10, 2), nullable=True, comment='商品单价快照(分)')
    excitation_income = Column(DECIMAL(10, 2), nullable=True, comment='奖励收入（分）')
    service_rate = Column(Float, nullable=True, comment='平台服务费率(千分比)')
    kwaimoney_user_id = Column(String(100), nullable=True)
    estimated_income = Column(DECIMAL(10, 2), nullable=True, comment='预估收入(分)')
    step_condition = Column(String(100), nullable=True, comment='阶梯佣金条件，0表示没有阶梯')

    update_strategy = UpdateStrategy.INCREMENTAL

    def __repr__(self):
        return f'<DwdCpsOrder(o_id="{self.o_id}, order_create_time="{self.order_create_time}", anchor_id="{self.anchor_id}")>'