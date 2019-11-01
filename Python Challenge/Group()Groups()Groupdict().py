# https://www.hackerrank.com/challenges/re-group-groups/problem

import re

res = re.search(r'([a-zA-Z0-9])\1+', input())
print(res.group(1) if res else -1)
