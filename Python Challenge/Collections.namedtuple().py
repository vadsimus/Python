# https://www.hackerrank.com/challenges/py-collections-namedtuple/problem

from collections import namedtuple

(n, categories) = (int(input()), input().split())
order = namedtuple('Order', categories)
marks = [int(order._make(input().split()).MARKS) for _ in range(n)]
print((sum(marks) / len(marks)))
