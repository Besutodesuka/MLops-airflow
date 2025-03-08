from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

def process():
    print("Processing data...")

# Define DAG
with DAG(
    dag_id="test_airflow_dag",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False
) as dag:

    start = PythonOperator(
        task_id="start",
        python_callable=lambda: print("Start task executed")
    )

    process_task = PythonOperator(
        task_id="process",
        python_callable=process
    )

    end = PythonOperator(
        task_id="end",
        python_callable=lambda: print("End task executed")
    )

    # Define Task Dependencies
    start >> process_task >> end