# https://www.hackerrank.com/challenges/any-or-all/problem

input()
s = list(map(str, input().split()))
print(all(int(i) > 0 for i in s) and any(i == i[::-1] for i in s))
