from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

# Add your script path to sys so Python can find your files
sys.path.insert(0, '/Users/spartan/Desktop/vscode/recession')

# Import your main functions from sentiment_etl and economic_etl
from sentiment_etl import main as run_sentiment_etl
from economic_etl import main as run_economic_etl

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

# Define the DAG
with DAG(
    dag_id='daily_sentiment_etl',
    default_args=default_args,
    description='Daily pull of financial headlines and economic indicators',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['sentiment', 'economics', 'etl']
) as dag:

    run_etl = PythonOperator(
        task_id='run_sentiment_etl_script',
        python_callable=run_sentiment_etl
    )

    run_econ_etl = PythonOperator(
        task_id='run_economic_etl_script',
        python_callable=run_economic_etl
    )

    run_etl >> run_econ_etl  # Define task order
