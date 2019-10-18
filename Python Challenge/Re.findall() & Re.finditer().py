# https://www.hackerrank.com/challenges/re-findall-re-finditer/problem

import re

string = 'abaabaabaabaae'
mass=re.findall(r'[aeuio]{2,}',string, re.I)
print('\n'.join(mass) if mass else '-1')