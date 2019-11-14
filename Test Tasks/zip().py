def my_zip(*args):
    result = []
    min_len = len(args[0])
    for i in args:
        if len(i) < min_len:
            min_len = len(i)
    for i in range(min_len):
        lst = []
        for k in args:
            lst.append(k[i])
        result.append(tuple(lst))
    return result


l1 = [x for x in range(1, 10)]
l2 = ['a', 'b', 'c', 'd', 'e', 'f']
l3 = ['one', 'two', 'three', 'four']
print(my_zip(l1, l2, l3))
