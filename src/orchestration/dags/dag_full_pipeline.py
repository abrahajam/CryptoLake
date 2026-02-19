"""
AG Master de CryptoLake — Fase 7.

Pipeline completo:
1. Init namespaces Iceberg
2. Ingesta batch (CoinGecko + Fear & Greed)
3. Bronze load (APIs → Iceberg)
4. Silver processing (Bronze → Silver con Spark)
5. Gold transformation (Silver → Gold con dbt)
6. Data quality checks (validadores custom)

Schedule: Diario a las 06:00 UTC
"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup

default_args = {
    "owner": "cryptolake",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(hours=1),
}

with DAG(
    dag_id="cryptolake_full_pipeline",
    default_args=default_args,
    description="Pipeline: Ingesta → Bronze → Silver → Gold → Quality",
    schedule="0 6 * * *",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["cryptolake", "production"],
    doc_md=__doc__,
) as dag:

    # ── INIT ────────────────────────────────────────────────
    init_namespaces = BashOperator(
        task_id="init_namespaces",
        bash_command=(
            "docker exec cryptolake-spark-master "
            "/opt/spark/bin/spark-submit --master 'local[1]' "
            "/opt/spark/work/src/processing/batch/init_namespaces.py"
        ),
    )

    # ── INGESTA ─────────────────────────────────────────────
    with TaskGroup("ingestion") as ingestion_group:
        extract_coingecko = BashOperator(
            task_id="extract_coingecko",
            bash_command=(
                "cd /opt/airflow && "
                "python -m src.ingestion.batch.coingecko_extractor"
            ),
        )
        extract_fear_greed = BashOperator(
            task_id="extract_fear_greed",
            bash_command=(
                "cd /opt/airflow && "
                "python -m src.ingestion.batch.fear_greed_extractor"
            ),
        )

    # ── BRONZE ──────────────────────────────────────────────
    with TaskGroup("bronze_load") as bronze_group:
        api_to_bronze = BashOperator(
            task_id="api_to_bronze",
            bash_command=(
                "docker exec cryptolake-spark-master "
                "/opt/spark/bin/spark-submit "
                "/opt/spark/work/src/processing/batch/api_to_bronze.py"
            ),
        )

    # ── SILVER ──────────────────────────────────────────────
    with TaskGroup("silver_processing") as silver_group:
        bronze_to_silver = BashOperator(
            task_id="bronze_to_silver",
            bash_command=(
                "docker exec cryptolake-spark-master "
                "/opt/spark/bin/spark-submit "
                "/opt/spark/work/src/processing/batch/bronze_to_silver.py"
            ),
        )

    # ── GOLD (dbt) ──────────────────────────────────────────
    with TaskGroup("gold_transformation") as gold_group:
        dbt_run = BashOperator(
            task_id="dbt_run",
            bash_command=(
                "export PYTHONNOUSERSITE=1 && "
                "cd /opt/airflow/src/transformation/dbt_cryptolake && "
                "/opt/dbt-venv/bin/dbt run --profiles-dir . --target prod"
            ),
        )
        dbt_test = BashOperator(
            task_id="dbt_test",
            bash_command=(
                "export PYTHONNOUSERSITE=1 && "
                "cd /opt/airflow/src/transformation/dbt_cryptolake && "
                "/opt/dbt-venv/bin/dbt test --profiles-dir . --target prod"
            ),
        )
        dbt_run >> dbt_test

    # ── DATA QUALITY (Fase 7) ───────────────────────────────
    with TaskGroup("data_quality") as quality_group:
        quality_checks = BashOperator(
            task_id="quality_checks",
            bash_command=(
                "docker exec cryptolake-spark-master "
                "/opt/spark/bin/spark-submit "
                "/opt/spark/work/src/quality/run_quality_checks.py"
            ),
        )

    # ── DEPENDENCIAS ────────────────────────────────────────
    (init_namespaces >> ingestion_group >> bronze_group
     >> silver_group >> gold_group >> quality_group)
