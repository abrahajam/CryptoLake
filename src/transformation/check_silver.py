"""Check if Silver tables exist and have data."""
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("check-silver") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

try:
    # List all tables in the silver namespace
    print("=== NAMESPACES IN CRYPTOLAKE ===")
    spark.sql("SHOW NAMESPACES IN cryptolake").show(truncate=False)

    print("\n=== TABLES IN cryptolake.silver ===")
    try:
        spark.sql("SHOW TABLES IN cryptolake.silver").show(truncate=False)
    except Exception as e:
        print(f"ERROR: {e}")

    print("\n=== daily_prices COUNT ===")
    try:
        c = spark.table("cryptolake.silver.daily_prices").count()
        print(f"Rows: {c}")
    except Exception as e:
        print(f"ERROR: {e}")

    print("\n=== fear_greed COUNT ===")
    try:
        c = spark.table("cryptolake.silver.fear_greed").count()
        print(f"Rows: {c}")
    except Exception as e:
        print(f"ERROR: {e}")

finally:
    spark.stop()
