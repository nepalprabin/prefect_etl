# A ETL pipeline using [prefect](https://www.prefect.io/)

This repository contains ETL pipeline for https://www.ncbi.nlm.nih.gov/geo/.

## Running data pipeline

1. Clone repo: <code> https://github.com/nepalprabin/prefect_etl.git</code>
2. cd prefect_etl
3. <code> pip install -r requirements.txt </code>
4. Setup prefect cloud backend: <code>prefect backend cloud</code>
5. Authenticate with Prefect Cloud: <code> prefect auth login --key YOUR-KEY </code> API key can be created by signing up at https://cloud.prefect.io/user/keys
6. Once authenticated run prefect UI on the cloud.