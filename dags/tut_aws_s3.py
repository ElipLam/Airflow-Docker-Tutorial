from datetime import datetime, timedelta
from textwrap import dedent
import boto3

# from handle_time import *

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
import pandas as pd

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator


BUCKET = "anltd-bucket"
PREFIX = "hackathon/player_heroes/"
CHECK_FILE = "check_download_player_heroes.parquet"
OUTPUT_FILE = "new_lake/players_heroes.parquet"

session = boto3.session.Session(
    aws_access_key_id="",
    aws_secret_access_key="",
    region_name="us-east-1",
)


def aws_get_object(bucket, key):
    s3 = session.resource("s3")
    obj = s3.Object(bucket, key).get()["Body"]
    return obj


def aws_read_object(obj):
    data = obj.read().decode("utf-8")
    return data


def aws_put_object(data, bucket, key):
    s3 = session.resource("s3")
    obj = s3.Object(bucket, key)
    obj.put(Body=data)
    pass


def aws_get_list_object(bucket, prefix=None):
    s3 = session.resource("s3")
    my_bucket = s3.Bucket(BUCKET)
    # list_keys = []
    if prefix == None:
        list_objects = my_bucket.objects.all()
    else:
        # get list objects
        list_objects = my_bucket.objects.filter(Prefix=prefix)

    list_keys = [s3_object.key for s3_object in list_objects]
    return list_keys


def aws_read_parquet(bucket, key):
    path = f"s3://{bucket}/{key}"
    df = wr.s3.read_parquet(path, boto3_session=session)
    return df


def aws_read_jsons(bucket, key):
    path = f"s3://{bucket}/{key}"
    df = wr.s3.read_json(path, boto3_session=session)
    return df


def aws_df_to_parquet(df, bucket, key):
    path = f"s3://{bucket}/{key}"
    wr.s3.to_parquet(df, path=path, boto3_session=session)
    pass


def aws_crawl_data(url, output_bucket, output_key, interval=1):
    download_start_time = time.time()
    response = requests.get(url, headers=None)

    # with open(output_path, "wb") as f:
    #     f.write(response.content)
    aws_put_object(response.content, output_bucket, output_key)
    download_end_time = time.time()
    elapsed_time = download_end_time - download_start_time
    if elapsed_time < interval:
        time.sleep(interval - elapsed_time)


# extract
def read_s3_file():
    obj = aws_get_object(BUCKET, "crawled_data/heroes.json")
    data = aws_read_object(obj)
    print(data)
    print(type(data))
    return data


# transform
def data_to_df(**kwargs):
    heroes_json = kwargs["ti"].xcom_pull(task_ids="read_s3_file")
    heroes_info = {"id": [], "name": [], "pro_win": [], "pro_pick": []}
    print(len(heroes_json))
    for hero in heroes_json:
        heroes_info["id"].append(hero["id"])
        heroes_info["name"].append(hero["name"])
        heroes_info["pro_win"].append(hero["pro_win"])
        heroes_info["pro_pick"].append(hero["pro_pick"])

    df_heroes = pd.DataFrame(heroes_info)

    df_heroes.loc[:, "name"] = df_heroes["name"].apply(
        lambda name: " ".join(name.split("_")[3:])
    )
    # df_heroes["WinrateAll"] = df_heroes["pro_win"].divide(df_heroes["pro_pick"])
    # df_heroes["WinrateAll"].fillna(0, inplace=True)
    df_heroes.rename(
        columns={
            "id": "HeroId",
            "name": "HeroName",
            "pro_win": "ProWin",
            "pro_pick": "ProPick",
        },
        inplace=True,
    )
    return df_heroes


# load
def save_s3_parquet(**kwargs):
    ti = kwargs["ti"].xcom_pull(task_ids="data_to_df")
    save_s3_parquet(data, BUCKET, "an_ltd.csv")
    # datetime_object = datetime.strptime(get_datetime_now(), "%Y-%m-%d %H:%M:%f")
    # year = datetime_object.year
    # month = datetime_object.month
    # day = datetime_object.day
    # hour = datetime_object.hour
    # minute = datetime_object.minute

    # df = pd.DataFrame([[year, month, day]])
    # df.to_csv(f"/opt/airflow/data/{year}_{month}_{day}_{hour}_{minute}.csv")
    # return year, month, day
    pass


with DAG(
    "anltd_s3_dag",
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

    task1 = PythonOperator(task_id="read_s3_file", python_callable=read_s3_file)
    task2 = PythonOperator(
        task_id="data_to_df",
        python_callable=data_to_df,
        op_kwargs={"alo": "con ga", "rep": "dai bang tra loi"},
    )
    task3 = PythonOperator(
        task_id="save_s3_parquet",
        python_callable=save_s3_parquet,
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
if __name__ == "__main__":
    read_s3_file()
