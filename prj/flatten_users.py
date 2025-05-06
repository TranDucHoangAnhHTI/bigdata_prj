import json

with open("merged_users.json", encoding="utf-8") as f_in, \
     open("user_lines.json", "w", encoding="utf-8") as f_out:
    arr = json.load(f_in)
    for obj in arr:
        f_out.write(json.dumps(obj, ensure_ascii=False) + "\n")
