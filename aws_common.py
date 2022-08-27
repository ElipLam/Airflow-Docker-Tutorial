from datetime import datetime
import pandas as pd
from pathlib import Path
import requests
import glob
import json
from progress.bar import IncrementalBar
import time
import sys
import awswrangler as wr
import boto3

# IaC
aws_section = "aws.amazon.com"
ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = Path(__file__).resolve().parents[0]
IAC_FOLDER = "IaC"
IAC_FILE_PATH = str(Path(ROOT, "IaC/credentials.ini"))
sys.path.append(str(Path(ROOT, IAC_FOLDER)))
from credentials import get_credentials

IMAGES_FOLDER = "images"
CRAWLED_DATA_FOLDER = "crawled_data"
LAKE_FOLDER = "lake"
NEW_LAKE_FOLDER = "new_lake"
SOURCE_FOLDER = "source_cloud"

# boto3
aws_credentails = get_credentials(IAC_FILE_PATH, aws_section)
session = boto3.session.Session(
    aws_access_key_id=aws_credentails["aws_access_key_id"],
    aws_secret_access_key=aws_credentails["aws_secret_access_key"],
    region_name=aws_credentails["region_name"],
)


BUCKET = "anltd-bucket"
PREFIX = "hackathon/player_heroes/"
CHECK_FILE = "check_download_player_heroes.parquet"
OUTPUT_FILE = "new_lake/players_heroes.parquet"


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


if __name__ == "__main__":
    print("You are in", BASE_PATH)
    pass
