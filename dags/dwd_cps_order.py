from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.utils.dates import days_ago
from . import utils as u


dag = DAG(
    dag_id='dwd_cps_order',
    description='ETL pipeline for ods_cps_order using SQL',
    schedule_interval='@daily',  # 每天运行
    start_date=days_ago(1),  # 开始日期
    catchup=False,  # 不补偿未执行的任务
)


dwd_cps_order_task = MySqlOperator(
    task_id='dwd_cps_order',
    mysql_conn_id='mysql',
    sql=u.read_sql_file('sql/dwd/dwd_cps_order.sql'),  # 执行的 SQL 查询
    autocommit=True,  # 确保事务自动提交
    dag=dag,
)


dwd_cps_order_task