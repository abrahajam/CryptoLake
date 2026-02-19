"""One-time bootstrap: create the 'default' namespace in the cryptolake catalog."""
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("create-default-ns") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

spark.sql("CREATE NAMESPACE IF NOT EXISTS cryptolake.default")
print("✅ Namespace cryptolake.default created successfully")
spark.stop()
