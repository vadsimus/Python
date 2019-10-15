# https://www.hackerrank.com/challenges/iterables-and-iterators/problem


from itertools import combinations


s=list(input().split())
n=int(input())
comb=list(combinations(s,n))
f=list(filter(lambda x: 'a' in x, comb))

print("{0:.4}".format(len(f)/len(comb)))
