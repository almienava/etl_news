from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy import DummyOperator
from src.scrape_file import sc_detik,sc_kompas
from src.transform_data import transform_news
from src.ingest_db_news import load_to_dwh


default_args = {
    'owner_email': 'Almienava',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=3)
}

dag = DAG(
    'ETL_News',
    description='ETL news to Database',
    start_date = datetime(2023,5,10),
    schedule_interval='0 23 * * *',
    default_args = default_args,
)

start_task = DummyOperator(task_id = 'Start_Task',)

scrape_detik_operator = PythonOperator(
    task_id='scrape_from_detik',
    python_callable=sc_detik,
    dag=dag,
)

scrape_kompas_operator = PythonOperator(
    task_id='scrape_from_kompas',
    python_callable=sc_kompas,
    dag=dag,
)

transform_operator = PythonOperator(
    task_id = 'transform_data',
    python_callable = transform_news,
    dag= dag,
)

load_dwh_operator = PythonOperator(
    task_id = 'loads_to_dwh',
    python_callable = load_to_dwh,
    dag= dag,
)


end_task = DummyOperator(task_id = 'End_Task',)

start_task >> [scrape_detik_operator,scrape_kompas_operator] >> transform_operator >> load_dwh_operator >> end_task