# https://www.hackerrank.com/challenges/alphabet-rangoli/problem

def print_rangoli(size):
    lines = []
    for k in range(size - 1, -1, -1):
        line = []
        for i in range(size + 96, 96 + k, -1):
            s = chr(i)
            line.append(s)
        r = []
        for i in range(len(line) - 2, -1, -1):
            r.append(line[i])
        line += r
        lines.append('-'.join(line).center((size * 4) - 3, '-'))
    bottom = []
    for i in range(len(lines) - 2, -1, -1):
        bottom.append(lines[i])
    lines += bottom
    for line in lines:
        print(str(line))


if __name__ == '__main__':
    n = int(input())
    print_rangoli(n)

