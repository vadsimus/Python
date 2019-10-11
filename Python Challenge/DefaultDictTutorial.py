# https://www.hackerrank.com/challenges/defaultdict-tutorial/problem
from collections import defaultdict

d = defaultdict(list)
n,m = map(int,input().split())
[d[input()].append(str(i)) for i in range(1,n+1)]

for _ in range(m):
    f=input()
    if not d[f]:
        print(-1)
        continue
    print(' '.join(d[f]))
