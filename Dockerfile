FROM apache/airflow:2.3.3

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    vim \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
USER airflow

FROM apache/airflow:2.3.3
COPY requirements.txt ./
# WORKDIR /opt/app
RUN python -m pip install --upgrade pip
# RUN pip install --no-cache-dir pyspark
# RUN pip install --no-cache-dir awswrangler
RUN pip install --no-cache-dir -r requirements.txt