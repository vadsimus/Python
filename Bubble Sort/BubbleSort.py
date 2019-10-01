import math
import os
import random
import re
import sys

# Complete the countSwaps function below.
def countSwaps(a):
    counter = 0
    for b in range(1,len(a)):
        for k in range(0, len(a)-b):
            if a[k] > a[k+1]:
                a[k], a[k+1] = a[k+1], a[k]
                counter += 1
    print("Array is sorted in {} swaps.".format(counter))
    print("First Element:", a[0])
    print("Last Element:", a[-1])

if __name__ == '__main__':
    n = int(input())

    a = list(map(int, input().rstrip().split()))

    countSwaps(a)

