from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, explode, struct, to_json
from pyspark.sql.types import StructType, StructField, StringType, BooleanType, ArrayType

# 1. Tạo SparkSession
spark = SparkSession.builder \
    .appName("KafkaToElasticsearchBulkCompatible") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# 2. Đọc dữ liệu từ Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "172.20.10.2:9092") \
    .option("subscribe", "twitter_user_data") \
    .option("startingOffsets", "earliest") \
    .load()

# 3. Parse JSON từ message
schema = ArrayType(StructType([
    StructField("username", StringType(), True),
    StructField("profile", StructType([
        StructField("profileUrl", StringType(), True),
        StructField("joinDate", StringType(), True),
        StructField("isVerified", BooleanType(), True),
        StructField("avatarUrl", StringType(), True),
        StructField("bannerUrl", StringType(), True),
        StructField("bio", StringType(), True),
        StructField("postCount", StringType(), True),
        StructField("followersCount", StringType(), True),
        StructField("followingCount", StringType(), True)
    ]), True),
    StructField("followers", ArrayType(StringType()), True),
    StructField("following", ArrayType(StringType()), True),
    StructField("tweets", ArrayType(StructType([
        StructField("profileLink", StringType(), True),
        StructField("replyCount", StringType(), True),
        StructField("hashtags", ArrayType(StringType()), True),
        StructField("mentions", ArrayType(StringType()), True),
        StructField("tweetText", StringType(), True),
        StructField("tweetTime", StringType(), True),
        StructField("likeCount", StringType(), True),
        StructField("repostCount", StringType(), True),
        StructField("viewCount", StringType(), True),
        StructField("media", StructType([
            StructField("images", ArrayType(StringType()), True)
        ]), True),
        StructField("type", StringType(), True),
        StructField("tweetID", StringType(), True)
    ])), True)
]))

parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("users"))
exploded_df = parsed_df.select(explode(col("users")).alias("user"))
bulk_ready_df = exploded_df.select(to_json(struct("user")).alias("json"))

# 4. Ghi log ra console và ghi vào Elasticsearch
def foreach_batch_function(batch_df, batch_id):
    print(f"\n[Batch ID]: {batch_id}")
    batch_df.show(truncate=False)

    batch_df.selectExpr("json as _doc").write \
        .format("org.elasticsearch.spark.sql") \
        .option("es.nodes", "localhost") \
        .option("es.port", "9200") \
        .option("es.resource", "twitter_users") \
        .option("es.index.auto.create", "true") \
        .option("es.nodes.wan.only", "true") \
        .mode("append") \
        .save()


# 5. Chạy Spark streaming
query = bulk_ready_df.writeStream \
    .foreachBatch(foreach_batch_function) \
    .outputMode("append") \
    .start()

query.awaitTermination()
