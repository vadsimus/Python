# https://www.hackerrank.com/challenges/merge-the-tools/problem


def merge_the_tools(string, k):
    for i in range(int(len(string) / k)):
        line_str = string[i * k:i * k + k]
        line = list(line_str)
        j = len(line) - 1
        while j > -1:
            if line.count(line[j]) >= 2:
                del line[j]
            j -= 1
        print(''.join(line))


if __name__ == '__main__':
    string, k = input(), int(input())
    merge_the_tools(string, k)
