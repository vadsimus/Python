# https://www.hackerrank.com/challenges/capitalize/problem

#!/bin/python3

import math
import os
import random
import re
import sys


# Complete the solve function below.
def solve(s):
    mass = list(s)
    pre = False
    mass[0]=mass[0].title()
    for i in range(len(mass)):
        if pre:
            mass[i] = mass[i].title()
            pre=False
        if mass[i] == ' ':
            pre = True
    return ''.join(mass)


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s = input()

    result = solve(s)

    fptr.write(result + '\n')

    fptr.close()
