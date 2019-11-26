# https://www.hackerrank.com/challenges/word-order/problem

from collections import defaultdict as dd

strings = dd(int)
for _ in range(int(input())):
    strings[input()] += 1

print(len(strings))
for i in strings:
    print(strings[i], end=' ')
