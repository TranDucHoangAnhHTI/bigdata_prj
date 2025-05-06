import json
import os
from kafka import KafkaProducer

# Config
KAFKA_BROKER = '172.20.10.2:9092'  # IP LAN máy Kafka
TOPIC_NAME = 'twitter_user_data'
JSON_FOLDER = 'D:/bigdata_prj/data'  # Đường dẫn thư mục chứa file .json


# Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Duyệt qua tất cả các file json
for filename in os.listdir(JSON_FOLDER):
    if filename.endswith(".json"):
        file_path = os.path.join(JSON_FOLDER, filename)
        with open(file_path, 'r') as f:
            data = json.load(f)
            producer.send(TOPIC_NAME, value=data)
            print(f"✅ Sent file: {filename}")

producer.flush()
producer.close()