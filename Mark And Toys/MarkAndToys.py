#https://www.hackerrank.com/challenges/mark-and-toys/problem
import math
import os
import random
import re
import sys

# Complete the maximumToys function below.
def maximumToys(prices, k):
    counter = 0
    sum = 0
    prices.sort()
    for i in range(len(prices)):
        sum+=prices[i]
        counter+=1
        if sum >= k:
            counter -= 1
            break
    return counter




if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    nk = input().split()

    n = int(nk[0])

    k = int(nk[1])

    prices = list(map(int, input().rstrip().split()))

    result = maximumToys(prices, k)

    fptr.write(str(result) + '\n')

    fptr.close()