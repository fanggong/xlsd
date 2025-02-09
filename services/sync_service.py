from services.update_service import UpdateService
from services.update_strategy import UpdateStrategy
from . import const as c

import logging

logger = logging.getLogger(__name__)

class SyncService:

    @staticmethod
    def get_data_fetcher(table_class):
        fetcher_class_path = c.FETCHERS.get(table_class.__tablename__)
        if not fetcher_class_path:
            raise ValueError(f'No data fetcher defined for table: {table_class.__tablename__}')

        module_name, class_name = fetcher_class_path.rsplit('.', 1)
        module = __import__(module_name, fromlist=[class_name])
        fetcher_class = getattr(module, class_name)
        return fetcher_class()

    @staticmethod
    def update_table(table_class, strategy: UpdateStrategy, **kwargs):
        data_fetcher = SyncService.get_data_fetcher(table_class)
        data_list = data_fetcher.fetch_data(**kwargs)
        logger.info(f'Data for table {table_class.__tablename__} GETODAZE!!!')

        if not data_list:
            logger.info('No data to update for table:', table_class.__tablename__)
            return

        logger.info(f'{strategy} update table {table_class.__tablename__}')
        try:
            if strategy == UpdateStrategy.FULL:
                UpdateService.full_update(table_class, data_list)
            elif strategy == UpdateStrategy.INCREMENTAL:
                UpdateService.incremental_update(table_class, data_list)
        except Exception as e:
            raise e

    @staticmethod
    def update_multiple_table(table_class, strategy, **kwargs):
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
                    UpdateService.full_update(key, data_list[index])
                elif value == UpdateStrategy.INCREMENTAL:
                    UpdateService.incremental_update(key, data_list[index])
            except Exception as e:
                raise e
