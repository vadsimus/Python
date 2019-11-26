# https://www.hackerrank.com/challenges/re-start-re-end/problem

import re

# s = input()
# k = input()
s = 'aaabaa'
k = 'aa'
m = re.search(r'({})'.format(k), s)
if m:
    for z in range(len(s)):
        m = re.search(r'({})'.format(k), s)
        if m :
            print((m.start(), m.end()-1,))
            s = s[:m.start()] + 'я' + s[m.start()+1:]
        else:
            break
else:
    print('(-1, -1)')