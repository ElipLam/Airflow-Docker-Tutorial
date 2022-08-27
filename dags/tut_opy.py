from datetime import datetime, timedelta
from textwrap import dedent

# from handle_time import *

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
import pandas as pd

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator


def get_datetime_now():
    today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    # a = "talent3"
    # return a
    # print("TIMEEEEEEEE:",today)
    return today


def print_datetime(**kwargs):
    # alo = kwargs["alo"]
    # rep = kwargs["rep"]
    ti = kwargs["ti"].xcom_pull(task_ids="get_datetime")
    return ti


def save_csv(**kwargs):
    value = kwargs["ti"].xcom_pull(task_ids="print_datetime")
    datetime_object = datetime.strptime(get_datetime_now(), "%Y-%m-%d %H:%M:%f")
    year = datetime_object.year
    month = datetime_object.month
    day = datetime_object.day
    hour = datetime_object.hour
    minute = datetime_object.minute

    df = pd.DataFrame([[year, month, day]])
    df.to_csv(f"/opt/airflow/data/{year}_{month}_{day}_{hour}_{minute}.csv")
    return year, month, day


with DAG(
    "anltd_datetime_dag",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        "owner": "AnLTD",
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 0,
        "retry_delay": timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success'
    },
    description="My DAG",
    schedule_interval=timedelta(seconds=60),
    start_date=datetime(2022, 8, 2),
    catchup=False,
    tags=["example"],
) as dag:

    task1 = PythonOperator(task_id="get_datetime", python_callable=get_datetime_now)
    task2 = PythonOperator(
        task_id="print_datetime",
        python_callable=print_datetime,
        op_kwargs={"alo": "con ga", "rep": "dai bang tra loi"},
    )
    task3 = PythonOperator(
        task_id="save_csv",
        python_callable=save_csv,
    )

    task1 >> task2 >> task3
    # # # t1, t2 and t3 are examples of tasks created by instantiating operators
    # t1 = BashOperator(
    #     task_id="print_date",
    #     bash_command="date",
    # )

    # t2 = BashOperator(
    #     task_id="sleep",
    #     depends_on_past=False,
    #     bash_command="sleep 5",
    #     retries=3,
    # )
    # t1.doc_md = dedent(
    #     """\
    # #### Task Documentation
    # You can document your task using the attributes `doc_md` (markdown),
    # `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
    # rendered in the UI's Task Instance Details page.
    # ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)

    # """
    # )

    # dag.doc_md = (
    #     __doc__  # providing that you have a docstring at the beginning of the DAG
    # )
    # dag.doc_md = """
    # This is a documentation placed anywhere
    # """  # otherwise, type it like this
    # templated_command = dedent(
    #     """
    # {% for i in range(5) %}
    #     echo "{{ ds }}"
    #     echo "{{ macros.ds_add(ds, 7)}}"
    # {% endfor %}
    # """
    # )

    # t3 = BashOperator(
    #     task_id="templated",
    #     depends_on_past=False,
    #     bash_command=templated_command,
    # )

    # t1 >> [t2, t3]
