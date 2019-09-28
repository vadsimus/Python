#!/bin/python3
#  https://www.hackerrank.com/challenges/count-triplets-1/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=dictionaries-hashmaps

import math
import os
import random
import re
import sys

# Complete the countTriplets function below.
def countTriplets(arr, r):
    ln=len(arr)
    counter=0
    p1=dict()
    p2=dict()
    for i in arr:
        w=i*r
        if i in p2:
            counter+=p2[i]
        if i in p1:            
            if w in p2:
                p2[w]+=p1[i]
            else:
                p2[w]=p1[i]
        if w in p1:
            p1[w]+=1
        else:
            p1[w]=1
    return counter

if __name__ == '__main__':
    

    nr = input().rstrip().split()

    n = int(nr[0])

    r = int(nr[1])

    arr = list(map(int, input().rstrip().split()))

    ans = countTriplets(arr, r)