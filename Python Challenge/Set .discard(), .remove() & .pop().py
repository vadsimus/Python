# https://www.hackerrank.com/challenges/py-set-discard-remove-pop/problem

n = int(input())
s = set(map(int, input().split()))
m=int(z.__next__())
for _ in range(m):
    command=list(input().split())
    if command[0]=='pop':
        s.pop()
    elif command[0]=='remove':
        s.remove(int(command[1]))
    elif command[0]=='discard':
        s.discard(int(command[1]))
print(sum(s))


