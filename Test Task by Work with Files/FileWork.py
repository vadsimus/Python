import re
from collections import defaultdict as dd
while True:
    file_name = input('File name:')

    try:
        with open(file_name, 'r') as file:
            ips = dd(int)
            # browsers = dd(int)

            oss = dd(int)
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
                    pass
                try:
                    os=re.split(r';', re.split(r'[()]', browser)[1])

                except IndexError:
                    pass
                else:
                    if os[0]=='compatible':
                        os=None
                    elif os[0]=='X11':
                        os=os[1]
                    else:
                        os=os[0]
                    if os:
                        os=[os.split()][0][0]
                        # print(os)

                        oss[os]+=1


               
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
print('Most popular OS:')
os_count=[x for x in oss.values()]
os_count.sort(reverse=True)
for i in range(5) if len(os_count)>5 else range(len(os_count)):
    os_found=[x for x in oss.keys() if oss[x] == os_count[i]][0]
    print(os_found,':',oss[os_found],'times')
    oss[os_found]=0

