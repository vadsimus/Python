# https://www.hackerrank.com/challenges/ginorts/problem

s = list(input())

a = [i for i in s if 97 <= ord(i) <= 122]
a.sort()
A = [i for i in s if 65 <= ord(i) <= 90]
A.sort()

dig_even = [i for i in s if i.isdigit() and int(i) % 2 != 0]
dig_even.sort()
dig_odd = [i for i in s if i.isdigit() and int(i) % 2 == 0]
dig_odd.sort()
print(''.join(a) + ''.join(A) + ''.join(dig_even) + ''.join(dig_odd))
