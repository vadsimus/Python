
#https://www.hackerrank.com/challenges/kangaroo/problem


import math
import os
import random
import re
import sys


def kangaroo(x1, v1, x2, v2):
    distance = x1-x2
    if abs(distance)==distance:
        m=True
    else:
        m=False
    if x1==x2:
        return "YES"
    if (x1<x2 and v1<v2) or (x1>x2 and v1>v2) or v1==v2:
        return "NO"
    count=0
    while True:
        count=count+1
       
        if (x1+v1*count)==(x2+v2*count):
            return "YES"
        pos=(x1+v1*count)-(x2+v2*count)
        if abs(pos)==pos and not m:
            return "NO"

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    x1V1X2V2 = input().split()

    x1 = int(x1V1X2V2[0])

    v1 = int(x1V1X2V2[1])

    x2 = int(x1V1X2V2[2])

    v2 = int(x1V1X2V2[3])

    result = kangaroo(x1, v1, x2, v2)

    fptr.write(result + '\n')

    fptr.close()
