import re
from collections import defaultdict as dd
while True:
    file_name = input('File name:')
    try:
        with open(file_name, 'r') as file:
            ips = dd(int)
            browsers = dd(int)
            for line in file:
                try:
                    ip = re.findall(r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', line)
                    ip = ip[0]
                except IndexError:
                    continue #IP is not found, this is wrong line, pass it.
                else:
                    ips[ip] += 1
                   
                browser = re.findall(r'[^""]+', line)               
                try:
                    browser = [browser[-2]][0]
                except IndexError:
                    pass
                else:
                    browsers[browser] += 1
               
            break #Stop cycle of file name input
    except FileNotFoundError:
        print('File not found')

print('Access:')
ip_count = [x for x in ips.values()]
ip_count.sort(reverse=True)
for i in range(10) if len(ip_count)>10 else range(len(ip_count)):
    ip_found=[x for x in ips.keys() if ips[x] == ip_count[i]][0]
    print(ip_found.ljust(15), end='')
    print(':',ips[ip_found],'times')
    ips[ip_found]=0
print('----------')
print('Most popular browsers:')
br_count=[x for x in browsers.values()]
br_count.sort(reverse=True)
for i in range(5) if len(br_count)>10 else range(len(br_count)):
    br_found=[x for x in browsers.keys() if browsers[x] == br_count[i]][0]
    print(br_found,':',browsers[br_found],'times')
    browsers[br_found]=0

