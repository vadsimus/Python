# https://www.hackerrank.com/challenges/re-sub-regex-substitution/problem

import re
n=int(input())
for _ in range(n):
    i = input()
    while True:
        j = re.sub(r'\s(\|\|)\s',' or ', i)
        if j == i:
            break
        i = j
    while True:
        k = re.sub(r'\s(\&\&)\s', ' and ', j)
        if k == j:
            break
        j = k
    print(k)