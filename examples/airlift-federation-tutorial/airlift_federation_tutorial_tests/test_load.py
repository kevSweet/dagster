import subprocess

import requests
from dagster_airlift.core import AirflowBasicAuthBackend, AirflowInstance
from dagster_airlift.in_airflow.gql_queries import VERIFICATION_QUERY
from airlift_federation_tutorial_tests.conftest import upstream_instance, downstream_instance, assert_successful_dag_run


def test_load_upstream(upstream_airflow: subprocess.Popen) -> None:
    af_instance = upstream_instance()
    assert len(af_instance.list_dags()) == 11
    assert_successful_dag_run(af_instance, "load_customers")



def test_load_downstream(downstream_airflow: subprocess.Popen) -> None:
    assert len(downstream_instance().list_dags()) == 11
    assert_successful_dag_run(downstream_instance(), "customer_metrics")




def test_load_dagster(dagster_dev: subprocess.Popen) -> None:
    response = requests.post(
        # Timeout in seconds
        "http://localhost:3000/graphql",
        json={"query": VERIFICATION_QUERY},
        timeout=3,
    )
    assert response.status_code == 200
