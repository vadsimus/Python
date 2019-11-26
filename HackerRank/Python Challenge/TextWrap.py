# https://www.hackerrank.com/challenges/text-wrap/problem


import textwrap

def wrap(string, max_width):
    col = len(string)//max_width
    st=string[:max_width]
    for i in range(1,col):
        st=st+'\n'+string[i*max_width:(i+1)*max_width]
    st=st+'\n'+string[(col*max_width):]
    return st

if __name__ == '__main__':
    string, max_width = input(), int(input())
    result = wrap(string, max_width)
    print(result)