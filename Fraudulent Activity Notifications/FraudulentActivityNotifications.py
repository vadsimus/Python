# https://www.hackerrank.com/challenges/fraudulent-activity-notifications/problem


# !/bin/python3

import math
import os
import random
import re
import sys


# Complete the activityNotifications function below.
def activityNotifications(expenditure, d):
    counter = 0
    exp = expenditure
    mass = [0] * 201
    for j in range(d):
        mass[exp[j]] += 1
    for i in range(d, len(exp)):
        indx = 0
        m = -1
        if d % 2 != 0:
            while indx < math.ceil(d / 2):
                m += 1
                indx += mass[m]
            median = m
        else:
            m = -1
            summ = 0
            flag = True
            pre = -1
            while summ < (d / 2) + 1:
                m += 1
                summ += mass[m]
                if summ >= (d/2)+1 and flag:
                    pre = m
                if summ == (d/2) and flag:
                    pre = m
                    flag = False
            median = (m + pre)/2
        if exp[i] >= median * 2:
            counter += 1
        mass[exp[i - d]] -= 1
        mass[exp[i]] += 1
    return counter

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    nd = input().split()

    n = int(nd[0])

    d = int(nd[1])

    expenditure = list(map(int, input().rstrip().split()))

    result = activityNotifications(expenditure, d)

    fptr.write(str(result) + '\n')

    fptr.close()
