from database.mysql import Base, engine
from models import *
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    Base.metadata.create_all(engine)