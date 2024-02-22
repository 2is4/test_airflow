from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta



ssh_command = "echo 'Hello from remote server'"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
    'start_date': datetime(2024, 1, 1),
}


dag = DAG(
   dag_id='SSH_DEMO',
   #(optional but highly recommended)
   default_args=default_args,
   description='A simple DAG',
   schedule_interval='@daily',
   start_date=datetime(2024, 1, 1),
   catchup=False
)

wait = BashOperator(
    task_id="wait",
    bash_command="sleep 30",
    retries=3,
    dag=dag
)

ssh_task = SSHOperator(
    task_id='ssh_task',
    ssh_conn_id='ssh_test',
    command='echo "Hello, world!" > myfile.txt',
    retries=3,  # Retries for SSH task
    dag=dag,
)

wait >> ssh_task
