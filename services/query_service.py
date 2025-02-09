from sqlalchemy import text
from database.mysql import db_session
import pandas as pd
from utils.decorators import retry


class QueryService:
    @staticmethod
    @retry(max_retries=5, delay=1)
    def execute_raw_sql(session, sql: str, params=None):
        try:
            result = session.execute(text(sql), params)
            return result.fetchall()
        finally:
            session.close()

    @staticmethod
    @retry(max_retries=5, delay=1)
    def fetch_df_dat(session, sql: str, params=None):
        try:
            connection = session.connection()
            return pd.read_sql(text(sql), con=connection, params=params)
        finally:
            session.close()