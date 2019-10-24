from urllib import request, parse
import sys
import re
import lxml.html
from datetime import datetime,timedelta


def create_date(string):
    try:
        dt = datetime.strptime(string, '%Y-%m-%d')
        return dt
    except ValueError or TypeError:
        return None

def input_date(prompt):
    while True:
        date = list(re.split('[ \-_]', input(prompt)))

        if date[0] == 'today':
            today = datetime.now()
            return '{}-{:0>2}-{:0>2}'.format(today.year, today.month, today.day)
        elif date[0].strip() == '':
            return None
        elif create_date('-'.join(date)):
            return '{}-{:0>2}-{:0>2}'.format(date[0], date[1], date[2])
        else:
            print('Wrong!!!')

def airport_input(prompt):
    airports=['AUH','DXB','DMM','ISB','JED','KHI','LHE','MED','MUX','MCT','PEW','RYK','UET','RUH','SHJ','SKT']
    print('Input airport (AUH,DXB,DMM,ISB,JED,KHI,LHE,MED,MUX,MCT,PEW,RYK,UET,RUH,SHJ,SKT) or help')
    while True:
        airport = input(prompt)
        for ap in airports:
            if airport.upper().strip() == ap:
                return ap
        if airport.lower() == 'help':
            print("""AUH - Abu Dhabi \nDXB - Dubai\nDMM - Dammam
ISB - Islmabad\nJED - Jeddah\nKHI - Karachi\nLHE - Lahore\nMED - Medina
MUX - Multan\nMCT - Muscat\nPEW - Peshawar\nRYK - Rahim Yar Khan
UET - Quetta\nRUH - Riyadh\nSHJ - Sharjah\nSKT - Sialkot""")


def get_document_from_site(my_params):
    myUrl = "https://www.airblue.com/bookings/flight_selection.aspx?"
    value = {'TT': 'RT', 'DC': 'KHI', 'AC': 'ISB', "AM": "2019-11", 'AD': '2',
             'RM': "2019-11", 'RD': '3', 'FL': 'on', 'CC': 'Y', 'CD': '',
             'PA': '1', 'PC': '', 'PI': '', 'x': '40', 'y': '20'}
    value['AD'] = my_params['AD']
    value['AM'] = my_params['AM']
    value['RM'] = my_params['RM']
    value['RD'] = my_params['RD']
    value['DC'] = my_params['DC']
    value['AC'] = my_params['AC']
    with open('Answer.html', "r") as file:
        otvet = file.read()

    # mydata = parse.urlencode(value)
    # myUrl = myUrl + mydata
    # req = request.Request(myUrl)
    # otvet = request.urlopen(req)
    # otvet = otvet.read().decode('UTF-8')

    with open('Answer.html', 'w') as file:
        file.write(otvet)

    doc = lxml.html.document_fromstring(otvet)
    return doc

def get_info_from_doc(doc,depart_date, roundtrip):
    flights = []

    if roundtrip:
        rtrp = '2'
    else:
        rtrp = '1'
    depart_date = depart_date.replace('-', '_')
    flights_counter = 1
    while True:
        flight_info = []
        try:
            xpath_base = '//*[@id="trip_{}_date_{}"]/tbody[{}]/tr/td'
            xpath_base = xpath_base.format(rtrp, depart_date, flights_counter)
            flight = doc.xpath('{}[1]/text()'.format(xpath_base))[0].strip()
            depart = doc.xpath('{}[2]/text()'.format(xpath_base))[0]
            arrive = doc.xpath('{}[4]/text()'.format(xpath_base))[0]

            k = 5
            flight_type = {}
            while True:
                try:

                    flight_class = doc.xpath(
                        '//*[@id="trip_{}_date_{}"]/thead/tr[2]/th[{}]/span/text()'.format(rtrp,
                            depart_date, k))[0]
                    coast = \
                        doc.xpath('{}[{}]/label/span/text()'.format(xpath_base, k + 1))[0]
                    currency = doc.xpath(
                        '{}[{}]/label/span/b/text()'.format(xpath_base, k + 1))[0]
                    flight_type[flight_class] = str(coast + " " + currency)
                    k += 1
                except IndexError:
                    break

            # print(depart_date, end=' | ')
            flight_info.append(depart_date)

            # print('flight:', flight, end=' | ')
            flight_info.append(flight)

            depart_time = datetime.strptime(depart.lower(), '%I:%M %p')
            # print('depart:', datetime.strftime(depart_time, '%H:%M'), end=' | ')
            flight_info.append(datetime.strftime(depart_time, '%H:%M'))

            arrive_time = datetime.strptime(arrive.lower(), '%I:%M %p')
            # print('arrive:', datetime.strftime(arrive_time, '%H:%M'), end=' | ')
            flight_info.append(datetime.strftime(arrive_time, '%H:%M'))

            time_in_flight = arrive_time - depart_time
            h_in_flight = time_in_flight.seconds // 3600
            m_in_flight = (time_in_flight.seconds // 60) % 60
            # print('Time in Flight: ', h_in_flight, "h ", m_in_flight, 'm', sep='', end=' | ')
            flight_info.append('{}h {}m'.format(h_in_flight,m_in_flight))


            for ft in flight_type:
                # print(ft, ":", flight_type[ft], end=" | ")
                flight_info.append(ft)
                flight_info.append(flight_type[ft])
            flights_counter += 1
            flights.append(flight_info)
        except IndexError:
            try:
                err = doc.xpath('//*[@id="content"]/div/div[2]/div/text()')
                if err:
                    print(err)
            except Exception:
                break

            break

    return flights



# departure = airport_input('Departure:')
departure='ISB'  #!!!!!!!!!!!!!!!!!!!!!!!
# arrive = airport_input('Destination:')
arrive = 'KHI'   #!!!!!!!!!!!!!!!!!!!!!!!
# while True:
#     depart_date = input_date('Date of flight out YYYY MM DD or today')
#     if depart_date:
#         break
#     else:
#         print("Depart date can't be empty")
depart_date='2019-10-25' #!!!!!!!!!!!!!!!!!!!!!!!

# back_date = input_date('Date to return back or empty')
back_date = '2019-10-27'
back_date_flag = True
if back_date == None:
    back_date_flag = False
    dep_date_datetime=create_date(depart_date)
    back_date = dep_date_datetime+timedelta(days=1)
    back_date = '{}-{:0>2}-{:0>2}'.format(back_date.year, back_date.month, back_date.day)



my_params = {}
my_params['AM'] = str(depart_date[:7])
my_params['AD'] = str(depart_date[8:])
my_params['RM'] = str(back_date[:7])
my_params['RD'] = str(back_date[8:])
my_params['DC'] = departure
my_params['AC'] = arrive



doc = get_document_from_site(my_params)
print(get_info_from_doc(doc,depart_date,False))
if back_date_flag:
    print('Back')
    get_info_from_doc(doc,back_date,True)


# except Exception:
#      print('AHTUNG')
#      print(sys.exc_info()[1])


# GET https://www.airblue.com/bookings/flight_selection.aspx?TT=RT&DC=KHI&AC=ISB&AM=2019-10&AD=23&RM=2019-10&RD=24&FL=on&CC=Y&CD=&PA=1&PC=&PI=&x=40&y=20 HTTP/1.1
# GET          /bookings/flight_selection.aspx?TT=RT&SS=&RT=&FL=on&DC=ISB&AC=DXB&AM=2019-11&AD=02&DC=&AC=&AM=&AD=&DC=&AC=&AM=&AD=&DC=&AC=&AM=&AD=&RM=2019-11&RD=04&PA=1&PC=&PI=&CC=&NS=&CD= HTTP/1.1
# //*[@id="trip_1_date_2019_11_02"]/tbody/tr/td[1]
