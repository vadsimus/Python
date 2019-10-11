# Enter your code here. Read input from STDIN. Print output to STDOUT
from collections import Counter

ss = []
q = int(input())
n = list(map(int, input().split()))
x = int(input())
for _ in range(x):
    ss.append(list(map(int, input().split())))
sizes = Counter(n)
result = 0
for i in range(len(ss)):
    if ss[i][0] in sizes.keys() and sizes[ss[i][0]] != 0:
        sizes[ss[i][0]] -= 1
        result += ss[i][1]
print(result)
