#!/usr/bin/env python
import sys, json

for line in sys.stdin:
    try:
        user = json.loads(line)
        uid = user.get("username")
        # header for bulk API
        hdr = {"index": {"_index": "twitter_users", "_id": uid}}
        print(json.dumps(hdr, ensure_ascii=False))
        # document body
        print(json.dumps(user, ensure_ascii=False))
    except:
        continue
