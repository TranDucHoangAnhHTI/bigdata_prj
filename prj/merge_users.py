import json
from pathlib import Path

# Load JSON từ file
def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

# Load từng phần dữ liệu
followers = load_json("data/followers.json")
following = load_json("data/following.json")
user_profile = load_json("data/userProfile.json")
tweet_data = load_json("data/tweetData.json")

# Xóa profile["username"] nếu có để tránh trùng lặp
user_profile.pop("username", None)

# Lấy username chính từ followers
username = followers["username"]

# Gộp dữ liệu theo user
merged_user = {
    "username": username,
    "profile": user_profile,
    "followers": followers.get("userIDs", []),
    "following": following.get("userIDs", []),
    "tweets": tweet_data.get("tweets", [])
}

# Ghi ra file mới
output_file = "merged_users.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump([merged_user], f, indent=2, ensure_ascii=False)

print(f"✅ Đã gộp thành công dữ liệu người dùng vào '{output_file}'")
