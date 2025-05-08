#!/usr/bin/env python
import sys, json

for line in sys.stdin:
    try:
        user = json.loads(line)
        uid = user.get("username")
        following = user.get("following", [])
        if uid and following:
            print(f"{uid}\t1.0\t{','.join(following)}")
    except Exception:
        continue
