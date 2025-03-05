from sqlalchemy import Column, String, Float, Integer, TIMESTAMP, Text
from sqlalchemy.dialects.mysql import BLOB, LONGTEXT, TINYINT
from database.mysql import Base
from services.update_strategy import UpdateStrategy



class OdsPlatformProducts(Base):
    __tablename__ = 'ods_platform_products'
    __table_args__ = {'comment': '产品'}
    
    id = Column(String(64), primary_key=True, default='', comment='产品ID')
    user_id = Column(String(64), nullable=False, default='', comment='所属用户')
    supplier_id = Column(String(64), default='', comment='所属供应商')
    brand = Column(String(64), default='', comment='品牌')
    name = Column(String(550), default='', comment='产品名称')
    class_ = Column('class', String(64), default='', comment='产品品类')
    mfr_name = Column(String(550), default='', comment='生产厂商名称')
    spec = Column(String(550), default='', comment='规格型号')
    spec_unit = Column(String(64), default='', comment='规格单位')
    filing_id = Column(String(128), default='', comment='产品备案号')
    batch_id = Column(String(128), default='', comment='生产批号')
    pro_date = Column(TIMESTAMP, nullable=True, comment='生产日期')
    exp_date = Column(TIMESTAMP, nullable=True, comment='到期日期')
    number = Column(String(550), default='', comment='产品编号')
    special = Column(TINYINT, default=0, comment='是否特批')
    anchor = Column(String(550), default='', comment='特批指定主播')
    price_normal = Column(Float, nullable=True, comment='日常价')
    price_sale = Column(Float, nullable=False, comment='直播价')
    com_ratio = Column(Float, nullable=False, comment='佣金比例')
    sale_text = Column(String(550), default='', comment='直播价文本')
    detail = Column(BLOB, comment='详细介绍')
    url_cover = Column(String(550), default='', comment='产品封面')
    url_card = Column(String(550), default='', comment='手卡图')
    url_real = Column(BLOB, comment='实物')
    url_outer = Column(BLOB, comment='外包装')
    url_inner = Column(BLOB, comment='内包装')
    third_test = Column(BLOB, comment='第三方检测报告')
    license_pro = Column(String(1100), default='', comment='生产许可')
    trademark = Column(String(1100), default='', comment='品牌商标注册证书')
    cert_auth = Column(String(2200), default='', comment='品牌生产授权证书')
    cert_filing = Column(String(1100), default='', comment='商品备案证书')
    annex = Column(BLOB, comment='附件')
    status = Column(TINYINT, nullable=False, default=0)
    by_anchor = Column(TINYINT, nullable=False, default=0, comment='是否是主播自采')
    ec_name = Column(String(64), default='', comment='电商名称')
    ec_mobile = Column(String(64), default='', comment='电商联系电话')
    ec_license = Column(String(550), default='', comment='电商营业执照')
    ec_contract = Column(TINYINT, nullable=True, comment='是否与电商签合同')
    pro_id = Column(String(550), default='', comment='产品ID')
    mfr_license = Column(String(550), default='', comment='生产厂商营业执照')
    machine = Column(String(550), default='', comment='机制')
    ref_id = Column(String(64), default='', comment='引用登记-被引用的商品id')
    settle_way = Column(String(64), default='', comment='结算方式')
    settle_date = Column(TIMESTAMP, nullable=True, comment='结算时间')
    inner_number = Column(String(550), default='', comment='仓库编码')
    inner_category = Column(String(128), default='', comment='仓库类目')
    wh_count = Column(Integer, nullable=True, comment='库存数量')
    is_sale = Column(TINYINT, default=1, comment='1（默认）-上架 | 0-下架')
    updated_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    anchor_live = Column(String(128), default='', comment='直播主播id：填报角色为供应商时：单选，所有平台已登录主播；填报角色为主播时：自动填充。')
    live_time = Column(TIMESTAMP, nullable=True, comment='开播时间')
    standers = Column(String(128), default='', comment='执行标准')
    remark = Column(String(550), default='', comment='备注')

    update_strategy = UpdateStrategy.INCREMENTAL

    def __repr__(self):
        return f'<OdsPlatformProducts(id="{self.id}, name="{self.name}"")>'