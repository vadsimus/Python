# https://www.hackerrank.com/challenges/no-idea/problem

from collections import defaultdict as dd

n, m = map(int, input().split())
mass = list(map(int, input().split()))
a = list(map(int, input().split()))
b = list(map(int, input().split()))

happiness = 0
dic = dd(int)
for i in mass:
    dic[i] += 1
for k in a:
    if k in dic.keys():
        happiness += dic[k]
for j in b:
    if j in dic.keys():
        happiness -= dic[j]
print(happiness)
