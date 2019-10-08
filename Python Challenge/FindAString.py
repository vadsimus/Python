# https://www.hackerrank.com/challenges/find-a-string/problem

def count_substring(string, sub_string):
    pos = 0
    i = 0
    counter = 0
    while pos < len(string):
        i = string.find(sub_string, pos)
        if i == -1:
            break
        counter += 1
        pos = i + 1
    return counter


if __name__ == '__main__':
    string = input().strip()
    sub_string = input().strip()

    count = count_substring(string, sub_string)
    print(count)