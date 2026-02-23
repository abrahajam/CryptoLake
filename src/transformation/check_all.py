"""Check all namespaces and tables in cryptolake catalog."""

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("check-all").master("local[*]").getOrCreate()

try:
    print("=== ALL NAMESPACES ===")
    spark.sql("SHOW NAMESPACES IN cryptolake").show(truncate=False)

    for ns in ["bronze", "silver", "gold", "default", "staging"]:
        print(f"\n=== TABLES IN cryptolake.{ns} ===")
        try:
            spark.sql(f"SHOW TABLES IN cryptolake.{ns}").show(truncate=False)
        except Exception as e:
            print(f"  ERROR: {type(e).__name__}: {e}")

    # Try direct SQL on bronze
    print("\n=== TRY SELECT FROM bronze.historical_prices ===")
    try:
        spark.sql("SELECT COUNT(*) as cnt FROM cryptolake.bronze.historical_prices").show()
    except Exception as e:
        print(f"  ERROR: {type(e).__name__}: {e}")

    # Check current catalog
    print("\n=== CURRENT CATALOG ===")
    spark.sql("SELECT current_catalog()").show()
    spark.sql("SELECT current_schema()").show()

finally:
    spark.stop()
