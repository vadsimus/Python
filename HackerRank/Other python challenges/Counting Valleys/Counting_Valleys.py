#https://www.hackerrank.com/challenges/counting-valleys/problem

import math
import os
import random
import re
import sys

def countingValleys(n, s):
    counter=0
    pos=0
   
    for a in s:
        if a=="D":
            pos-=1
        elif a=="U":
            pos+=1
            if pos==0:
                counter+=1
        else: raise(ValueError)
        

    return counter

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input())

    s = input()

    result = countingValleys(n, s)

    fptr.write(str(result) + '\n')

    fptr.close()

