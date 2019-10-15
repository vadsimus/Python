# https://www.hackerrank.com/challenges/compress-the-string/problem

from itertools import groupby

string = input()
result = []
result = [list((k, list(g))) for k, g in groupby(string)]

for i in result:
    print('(' + str(len(i[1])) + ',' + i[0] + ')', end=' ')
