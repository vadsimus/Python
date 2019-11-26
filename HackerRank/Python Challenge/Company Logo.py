# https://www.hackerrank.com/challenges/most-commons/problem


from collections import defaultdict as dd

if __name__ == '__main__':
    s = input()
    dic = dd(int)
    for ch in s:
        dic[ch] += 1
    result = []
    for _ in range(len(dic)) if len(dic) < 3 else range(3):
        max_value = max(dic.values())
        if max_value == 0:
            break
        cur = [[k, v] for k, v in dic.items() if v == max_value]
        cur.sort(key=lambda x: x[0])
        for i in cur:
            result.append(i)
            dic[i[0]] = 0

    for i in range(len(result)) if len(result) < 3 else range(3):
        print(result[i][0], result[i][1])
