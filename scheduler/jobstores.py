from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from config import Config

jobstores = {
    'default': SQLAlchemyJobStore(url=Config.get_mysql_url())
}
