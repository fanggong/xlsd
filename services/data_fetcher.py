from abc import ABC, abstractmethod
from datetime import datetime


class DataFetcher(ABC):
    @abstractmethod
    def fetch_data(self, **kwargs):
        pass

    @abstractmethod
    def process_data(self, **kwargs):
        pass

    @staticmethod
    def process_keys(item, key_mapping):
        return {
            key_mapping[k]: None if v in ['', '-'] else v
            for k, v in item.items()
            if k in key_mapping
        }

    @staticmethod
    def from_timestamp(x):
        try:
            result = datetime.fromtimestamp(int(x) / 1000)
        except ValueError:
            result = None
        return result