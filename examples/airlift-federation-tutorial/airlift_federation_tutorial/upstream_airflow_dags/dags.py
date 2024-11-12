import os

import duckdb
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airlift_federation_tutorial.constants import (
    CUSTOMERS_COLS,
    CUSTOMERS_CSV_PATH,
    CUSTOMERS_DB_NAME,
    CUSTOMERS_SCHEMA,
    CUSTOMERS_TABLE_NAME,
    DUCKDB_PATH,
)


def load_customers() -> None:
    # https://github.com/apache/airflow/discussions/24463
    os.environ["NO_PROXY"] = "*"
    df = pd.read_csv(  # noqa: F841 # used by duckdb
        CUSTOMERS_CSV_PATH,
        names=CUSTOMERS_COLS,
    )

    # Connect to DuckDB and create a new table
    con = duckdb.connect(str(DUCKDB_PATH))
    con.execute(f"CREATE SCHEMA IF NOT EXISTS {CUSTOMERS_SCHEMA}").fetchall()
    con.execute(
        f"CREATE TABLE IF NOT EXISTS {CUSTOMERS_DB_NAME}.{CUSTOMERS_SCHEMA}.{CUSTOMERS_TABLE_NAME} AS SELECT * FROM df"
    ).fetchall()
    con.close()


with DAG(
    dag_id="load_customers",
    is_paused_upon_creation=False,
) as dag:
    PythonOperator(
        task_id="load_customers_to_warehouse",
        python_callable=load_customers,
        dag=dag,
    )

for i in range(10):
    with DAG(
        dag_id=f"unrelated_{i}",
        is_paused_upon_creation=False,
    ) as dag:
        PythonOperator(
            task_id=f"task_{i}",
            python_callable=lambda: None,
            dag=dag,
        )
    globals()[f"unrelated_{i}"] = dag
