# https://www.hackerrank.com/challenges/py-collections-ordereddict/problem

from collections import defaultdict


def input_tests():
    string = """9
BANANA FRIES 12
POTATO CHIPS 30
APPLE JUICE 10
CANDY 5
APPLE JUICE 10
CANDY 5
CANDY 5
CANDY 5
POTATO CHIPS 30"""
    string = string.split('\n')
    for i in range(len(string)):
        yield string[i]


z = input_tests()  # Creating iterable object for emulating input for test
n = int(z.__next__())
d = defaultdict(int)
for _ in range(n):
    inp = z.__next__().split()
    price = int(inp[-1])
    name = str(' '.join(inp[:-1]))
    d[name] += price
for i in d:
    print(i, d[i])
