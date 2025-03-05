from sqlalchemy import Column, DECIMAL, String, DateTime, BigInteger, Float
from database.mysql import Base
from services.update_strategy import UpdateStrategy

class DwdCpsOrder(Base):
    __tablename__ = 'dwd_cps_order'

    order_create_time = Column(DateTime, nullable=True, comment='订单创建时间')
    o_id = Column(String(100), primary_key=True, nullable=False, comment='订单ID')
    item_id = Column(String(100), nullable=False, comment='商品ID')
    item_title = Column(String(100), nullable=False, comment='商品标题')

    def __repr__(self):
        return f'<DwdCpsOrder(o_id="{self.o_id}, order_create_time="{self.order_create_time}", anchor_id="{self.anchor_id}")>'