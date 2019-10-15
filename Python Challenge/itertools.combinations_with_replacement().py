# https://www.hackerrank.com/challenges/itertools-combinations-with-replacement/problem

from itertools import combinations_with_replacement

string, n = input().split()
n = int(n)
result = []
c = combinations_with_replacement(string, n)
for i in c:
    tmp = list(i)
    tmp.sort()
    result.append(''.join(tmp))
result.sort()
for i in result:
    print(i)
