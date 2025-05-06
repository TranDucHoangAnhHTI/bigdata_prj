import json

# Đọc dữ liệu từ file merged_users.json
with open("merged_users.json", "r", encoding="utf-8") as f:
    users = json.load(f)

# Tạo file phù hợp Bulk API
with open("bulk_users.json", "w", encoding="utf-8") as f:
    for user in users:
        meta = { "index": { "_index": "twitter_users" } }
        f.write(json.dumps(meta) + "\n")
        f.write(json.dumps(user, ensure_ascii=False) + "\n")

print("✅ Đã tạo file bulk_users.json sẵn sàng để upload vào Elasticsearch.")
