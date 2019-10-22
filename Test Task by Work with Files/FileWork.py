import re
from collections import defaultdict as dd


def print_popular_items_from_dic(title: str, dic: dict, n: int):
    """Print n elements from dictionary, which have max value.
    This dictionary would be broken after print. Use copy if you need
    dictionary somewhere else.
    :param title: Title of print.
    :param dic: Dictionary where would be found and print most popular items.
    :param n: Number items to print.
    """
    print(title)
    item_count = [x for x in dic.values()]
    item_count.sort(reverse=True)
    for i in range(n) if len(item_count) > n else range(len(item_count)):
        item_found = [x for x in dic.keys() if dic[x] == item_count[i]][0]
        print(item_found.ljust(20), ':', dic[item_found], 'times')
        dic[item_found] = 0
    print('-' * 20)
    dic.clear()


if __name__ == '__main__':
    while True:
        file_name = input('File name:')
        try:
            with open(file_name, 'r') as file:
                ips = dd(int)
                oss = dd(int)
                for line in file:
                    ip = re.search(r'\d+\.\d+\.\d+\.\d+', line)
                    try:
                        ip = ip[0]
                    except IndexError:
                        ip = None
                    else:
                        if ip:
                            ips[ip] += 1
                    browser = re.findall(r'[^"]+', line)
                    try:
                        browser = [browser[-2]][0]
                        os = re.split(r';', re.split(r'[()]', browser)[1])
                        if 'compatible' in ' '.join(os):
                            os = None
                        elif os[0] == 'X11':
                            if os[1] == ' U':
                                os = os[2]
                            else:
                                os = os[1]
                        else:
                            os = os[0]
                    except IndexError:
                        os = None
                    else:
                        if os:
                            os = [os.split()][0][0]
                            oss[os] += 1
                break  # Stop cycle of file name input.
        except FileNotFoundError:
            print('File not found, try again')

    print_popular_items_from_dic('Access:', ips, 10)
    print_popular_items_from_dic('Most popular OS:', oss, 5)