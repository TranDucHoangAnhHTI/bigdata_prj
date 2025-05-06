from kafka import KafkaConsumer
import json

# Config
KAFKA_BROKER = '172.20.10.2:9092'  # Địa chỉ IP LAN của máy đang chạy Kafka
TOPIC_NAME = 'twitter_user_data'

# Kafka consumer
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=[KAFKA_BROKER],
    auto_offset_reset='earliest',  # bắt đầu từ đầu topic nếu chưa có offset
    enable_auto_commit=True,
    group_id='twitter-consumer-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("👂 Listening for messages on topic:", TOPIC_NAME)
print("=============================================")

for message in consumer:
    print("📥 Received:")
    print(json.dumps(message.value, indent=2))