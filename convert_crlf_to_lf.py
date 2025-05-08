import json

with open("merged_users.json", "r", encoding="utf-8") as f:
    data = json.load(f)  # đọc toàn bộ mảng

with open("merged_users_lines.json", "w", encoding="utf-8") as f:
    for item in data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
