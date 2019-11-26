# https://www.hackerrank.com/challenges/itertools-combinations/problem

from itertools import combinations

string, n = map(str, input().split())
n = int(n)
result = []
for i in range(1, n + 1):
    r = list(combinations(string, i))
    tmp = []
    for i in r:
        e = list(i)
        e.sort()
        e = ''.join(e)
        tmp.append(e)
    tmp.sort()
    result += tmp

for i in result:
    print(''.join(i))
