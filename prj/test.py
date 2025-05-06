from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("TestPySpark") \
    .getOrCreate()

print(spark.range(5).collect())
spark.stop()
