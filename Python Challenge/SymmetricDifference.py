# https://www.hackerrank.com/challenges/symmetric-difference/problem


m = int(input())
M = list(map(int, input().split()))
n = int(input())
N = list(map(int, input().split()))
a = set()
b = set()
for i in M:
    a.add(i)
for i in N:
    b.add(i)

c = (a.difference(b)).union(b.difference(a))
mass = list(c)
mass.sort()
for i in mass:
    print(i)
