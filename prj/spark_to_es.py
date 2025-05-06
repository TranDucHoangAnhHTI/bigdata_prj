from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("BatchToElasticsearch") \
        .master("spark://spark-master:7077") \
        .config("spark.es.nodes", "elasticsearch") \
        .config("spark.es.port", "9200") \
        .getOrCreate()

    df = spark.read.parquet("hdfs://hadoop-namenode:8020/user/smartgrid/batch_result.parquet")

    # In ra số dòng để kiểm tra
    print("Row count:", df.count())
    df.show(10)

    df.write \
      .format("org.elasticsearch.spark.sql") \
      .option("es.resource", "smartgrid-batch") \
      .option("es.index.auto.create", "true") \
      .mode("overwrite") \
      .save()

    spark.stop()
