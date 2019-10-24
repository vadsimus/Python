from urllib import request, parse
import sys
import re
# import xml.etree.ElementTree as ET
import lxml.html
from datetime import datetime




depart_date=list(re.split(' |-|_',input('Date of flight out YYYY MM DD')))
# depart_date = '_'.join(depart_date)



today = datetime.now()
# depart_date = '{}_{}_{}'.format(today.year, today.month, today.day)
depart_date = '{}-{:0>2}-{:0>2}'.format(depart_date[0], depart_date[1], depart_date[2])


myUrl = "https://www.airblue.com/bookings/flight_selection.aspx?"
value = {'TT': 'RT', 'DC': 'KHI', 'AC': 'ISB', "AM": "2019-11", 'AD': '2',
         'RM': "2019-11", 'RD': '3', 'FL': 'on', 'CC': 'Y', 'CD': '',
         'PA': '1', 'PC': '', 'PI': '', 'x': '40', 'y': '20'}
value['AM'] = str(depart_date[:7])
value['AD'] = str(depart_date[8:])
print(value['AD'])
print(value['AM'])

# try:

# with open('Flight Selection4.html', "r") as file:
#     otvet = file.read()


mydata = parse.urlencode(value)
myUrl = myUrl + mydata
req = request.Request(myUrl)
otvet = request.urlopen(req)
otvet = otvet.read().decode('UTF-8')

with open('Answer.html','w') as file:
    file.write(otvet)

doc = lxml.html.document_fromstring(otvet)

flights_counter = 1

while True:
    try:

        xpath_base = '//*[@id="trip_1_date_{}"]/tbody[{}]/tr/td'.format(
            depart_date, flights_counter)

        flight = doc.xpath('{}[1]/text()'.format(xpath_base))[0].strip()
        depart = doc.xpath('{}[2]/text()'.format(xpath_base))[0]
        arrive = doc.xpath('{}[4]/text()'.format(xpath_base))[0]




        k = 5
        flight_type = {}
        while True:
            try:
                flight_class = doc.xpath(
                    '//*[@id="trip_1_date_{}"]/thead/tr[2]/th[{}]/span/text()'.format(
                        depart_date, k))[0]
                coast = \
                doc.xpath('{}[{}]/label/span/text()'.format(xpath_base, k + 1))[
                    0]
                currency = doc.xpath(
                    '{}[{}]/label/span/b/text()'.format(xpath_base, k + 1))[0]
                flight_type[flight_class] = str(coast + " " + currency)
                k += 1
            except Exception:

                break
        # // *[ @ id = "trip_1_date_2019_10_25"] / tbody[2] / tr / td[1]
        print(depart_date, end=' | ')
        print('flight:', flight, end=' | ')

        depart_time=datetime.strptime(depart.lower(),'%I:%M %p')

        print('depart:', datetime.strftime(depart_time, '%H:%M'), end=' | ')

        arrive_time=datetime.strptime(arrive.lower(),'%I:%M %p')

        print('arrive:', datetime.strftime(arrive_time,'%H:%M'), end=' | ')

        time_in_flight = arrive_time - depart_time
        h_in_flight=time_in_flight.seconds//3600
        m_in_flight=(time_in_flight.seconds//60)%60
        print('Time in Flight: ',h_in_flight,"h ",m_in_flight,'m', sep='',end=' | ')


        for ft in flight_type:
            print(ft, ":", flight_type[ft], end=" | ")
        print()
        flights_counter += 1
    except Exception:
        try:
            err=doc.xpath('//*[@id="content"]/div/div[2]/div/text()')
            print(err)
        except Exception:
            break

        break

# except Exception:
#      print('AHTUNG')
#      print(sys.exc_info()[1])


# GET https://www.airblue.com/bookings/flight_selection.aspx?TT=RT&DC=KHI&AC=ISB&AM=2019-10&AD=23&RM=2019-10&RD=24&FL=on&CC=Y&CD=&PA=1&PC=&PI=&x=40&y=20 HTTP/1.1
# GET          /bookings/flight_selection.aspx?TT=RT&SS=&RT=&FL=on&DC=ISB&AC=DXB&AM=2019-11&AD=02&DC=&AC=&AM=&AD=&DC=&AC=&AM=&AD=&DC=&AC=&AM=&AD=&RM=2019-11&RD=04&PA=1&PC=&PI=&CC=&NS=&CD= HTTP/1.1
# //*[@id="trip_1_date_2019_11_02"]/tbody/tr/td[1]