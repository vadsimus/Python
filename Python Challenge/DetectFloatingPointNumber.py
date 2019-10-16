# https://www.hackerrank.com/challenges/introduction-to-regex/problem

for _ in range(int(input())):
    f = input()
    ans = True
    if not ('.' in f and f.count('.') == 1):
        print('False')
        continue
    if f[0] == "+" or f[0] == "-":

        c, d = f[1:].split('.')
        if not (all(x.isdigit() for x in c) and all(x.isdigit() for x in d)):
            print('False')
            continue
    else:

        c, d = inp = f.split('.')
        if not (all(x.isdigit() for x in c) and all(x.isdigit() for x in d)):
            print('False')
            continue
    print('True')
