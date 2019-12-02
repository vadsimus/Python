import re

n = int(input())
for _ in range(n):
    print('YES' if re.fullmatch(r'[789]\d{9}', input()) else 'NO')


