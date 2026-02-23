"""Minimal check: does bronze namespace exist?"""
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("q").master("local[*]").getOrCreate()
print("NAMESPACES:")
for row in spark.sql("SHOW NAMESPACES IN cryptolake").collect():
    print(f"  - {row[0]}")
print("\nBRONZE TABLES:")
try:
    for row in spark.sql("SHOW TABLES IN cryptolake.bronze").collect():
        print(f"  - {row[1]}")
except Exception as e:
    print(f"  ERROR: {e}")
spark.stop()
