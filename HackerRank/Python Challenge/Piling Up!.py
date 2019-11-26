# https://www.hackerrank.com/challenges/piling-up/problem


n = int(input())
for _ in range(n):
    answer = True
    input()
    line = list(map(int, input().split()))
    while len(line) > 1:
        if line[0] >= line[1]:
            del line[0]
            continue
        elif line[-1] >= line[-2]:
            del line[-1]
            continue
        answer = False
        break
    print("Yes" if answer else 'No')
