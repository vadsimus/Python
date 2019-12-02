import re

n = int(input())
for _ in range(n):
    name, email = input().split()

    if re.fullmatch(r'<[a-zA-Z][\w\-._]+@[a-zA-Z]+(\.[a-zA-Z]{1,3}){1,2}>',
                    email):
        print(name, email)
