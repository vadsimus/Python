# https://www.hackerrank.com/challenges/py-the-captains-room/problem


from collections import defaultdict

k = int(input())
s = list(map(int, input().split()))
dic = defaultdict(int)
for i in s:
    dic[i] += 1

print([x for x in dic.keys() if dic[x] == 1][0])
