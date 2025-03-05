from sqlalchemy import Column, String, DECIMAL, Integer, TIMESTAMP
from sqlalchemy.dialects.mssql import TINYINT
from database.mysql import Base
from services.update_strategy import UpdateStrategy


class OdsKsAnchorInfo(Base):
    __tablename__ = 'ods_ks_anchor_info'
    
    anchor_id = Column(String(255), primary_key=True, comment='其实就是平台的user_id')
    anchor_name = Column(String(255), nullable=True, comment='主播名')
    anchor_type = Column(String(10), nullable=True, comment='类型')
    group_leader = Column(String(255), default='', comment='组长')
    specific_bd = Column(String(255), default='', comment='专属商务')
    specific_op = Column(String(255), default='', comment='专属运营')
    anchor_commission_rate = Column(DECIMAL(10, 2), nullable=True, comment='主播分成比例')
    organization_commission_rate = Column(DECIMAL(10, 3), nullable=True, comment='公司分成比例')
    other_commission_rate = Column(DECIMAL(10, 0), nullable=True, comment='其他分成比例')
    other_commission_belong = Column(String(255), default='', comment='其他分成的归属')
    status = Column(TINYINT, nullable=True, comment='状态：1-正常 | 2-解约中 | 3-已解约')
    line = Column(Integer, nullable=True, comment='业务线：0=老板周边；1=直播电商；2=切片；3=其它业务')
    sequence = Column(TINYINT, default=0, comment='排序')
    updated_at = Column(TIMESTAMP, nullable=True, onupdate='CURRENT_TIMESTAMP', comment='更新时间')

    update_strategy = UpdateStrategy.FULL

    def __repr__(self):
        return f'<OdsKsAnchorInfo(anchor_id="{self.anchor_id}, anchor_name="{self.anchor_name}")>'