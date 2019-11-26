# https://www.hackerrank.com/challenges/designer-door-mat/problem

n, m = map(int, input().split())

h = int((n - 1) / 2)
for i in range(0, h):
    print('---' * (h - i) + ".|." * i + '.|.' + '.|.' * i + '---' * (h - i))
print("-" * int((m - 7) / 2) + 'WELCOME' + "-" * int((m - 7) / 2))
for i in range(h - 1, -1, -1):
    print('---' * (h - i) + ".|." * i + '.|.' + '.|.' * i + '---' * (h - i))
