from services.update_strategy import UpdateStrategy
from . import const as c
from utils.decorators import retry
from sqlalchemy.dialects.mysql import insert
from datetime import datetime

import time
import logging


logger = logging.getLogger(__name__)

class SyncService:
    def __init__(self, session):
        self.session = session

    @retry(max_retries=5, delay=1)
    def full_update(self, table_class, data_list):
        logger.info(f'full update sync table {table_class}...')
        session = self.session
        try:
            with session().begin_nested():
                session().query(table_class).delete()
                for data in data_list:
                    time.sleep(0)
                    new_record = table_class(**data)
                    session().add(new_record)
            session().commit()
        except Exception as e:
            session().rollback()
            raise e
        finally:
            session.remove()

    @retry(max_retries=5, delay=1)
    def incremental_update(self, table_class, data_list):
        logger.info(f'incremental update sync table {table_class}...')
        session = self.session
        try:
            for data in data_list:
                time.sleep(0)
                insert_stmt = insert(table_class).values(**data)
                update_stmt = {key: insert_stmt.inserted[key] for key in data}
                session().execute(insert_stmt.on_duplicate_key_update(**update_stmt))
            session().commit()
        except Exception as e:
            session().rollback()
            raise e
        finally:
            session.remove()

    @staticmethod
    def get_data_fetcher(table_class):
        fetcher_class_path = c.FETCHERS.get(table_class.__tablename__)
        if not fetcher_class_path:
            raise ValueError(f'No data fetcher defined for table: {table_class.__tablename__}')

        module_name, class_name = fetcher_class_path.rsplit('.', 1)
        module = __import__(module_name, fromlist=[class_name])
        fetcher_class = getattr(module, class_name)
        return fetcher_class

    def update_table(self, table_class, strategy: UpdateStrategy, init_fetcher, **kwargs):
        data_fetcher = SyncService.get_data_fetcher(table_class)
        data_list = data_fetcher(**init_fetcher).fetch_data(**kwargs)
        logger.info(f'Data for table {table_class.__tablename__} GETODAZE!!!')

        if not data_list:
            logger.info(f'No data to update for table: {table_class.__tablename__}')
            return

        logger.info(f'{strategy} update table {table_class.__tablename__}')
        try:
            if strategy == UpdateStrategy.FULL:
                self.full_update(table_class, data_list)
            elif strategy == UpdateStrategy.INCREMENTAL:
                self.incremental_update(table_class, data_list)
        except Exception as e:
            raise e

    def update_multiple_table(self, table_class, strategy, **kwargs):
        data_fetcher = SyncService.get_data_fetcher(table_class)
        data_list = data_fetcher.fetch_data(**kwargs)
        logger.info(f'Data for table {table_class.__tablename__} GETODAZE')

        if not data_list:
            logger.info("No data to update for table:", table_class.__tablename__)
            return

        for index, (key, value) in enumerate(strategy.items()):
            logger.info(f'{value} update table {key.__tablename__}')
            try:
                if value == UpdateStrategy.FULL:
                    self.full_update(key, data_list[index])
                elif value == UpdateStrategy.INCREMENTAL:
                    self.incremental_update(key, data_list[index])
            except Exception as e:
                raise e
