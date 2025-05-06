from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count

if __name__ == "__main__":
    # 1. Tạo SparkSession, trỏ đến Spark Master
    spark = SparkSession.builder \
        .appName("BatchProcessingSmartGrid") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

    # 2. Đọc dữ liệu CSV từ HDFS
    # Giả sử file nằm ở /user/smartgrid/smartgrid_data.csv
    df = spark.read \
        .option("header", True) \
        .option("inferSchema", True) \
        .csv("hdfs://hadoop-namenode:8020/user/smartgrid/smartgrid_data.csv")

    # 3. In schema (tuỳ chọn, để kiểm tra)
    df.printSchema()

    # 4. Thực hiện tính toán (ví dụ: trung bình cột 'power' và đếm số record theo location)
    agg_df = df.groupBy("location") \
               .agg(avg("power").alias("avg_power"), count("*").alias("count_records"))

    # 5. Lưu kết quả (precompute view) vào HDFS dưới dạng Parquet
    agg_df.write.mode("overwrite").parquet("hdfs://hadoop-namenode:8020/user/smartgrid/batch_result.parquet")

    spark.stop()
