# https://www.hackerrank.com/challenges/zipped/problem

n, x = map(int, input().split())
lines = []
for _ in range(x):
    scores = list(map(float, input().split()))
    lines.append(scores)

z = list(zip(*lines))

for i in range(n):
    print(sum(z[i]) / x)
