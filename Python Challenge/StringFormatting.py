# https://www.hackerrank.com/challenges/python-string-formatting/problem

def print_formatted(number):
    for i in range(1,number+1):
        ln=len(bin(number))-2
        d=str(i)
        o=str(oct(i))
        h=str(hex(i))
        b=str(bin(i))
        print(d.rjust(ln),o[2:].rjust(ln),h.upper()[2:].rjust(ln),b[2:].rjust(ln))


if __name__ == '__main__':
    n = int(input())
    print_formatted(n)