from urllib import request, parse
import sys
import re
import lxml.html
from datetime import datetime, timedelta


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
    airports = {'AUH':'Abu Dhabi', 'DXB':'Dubai', 'DMM':'Dammam',
                'ISB':'Islmabad', 'JED':'Jeddah', 'KHI':'Karachi',
                'LHE':'Lahore', 'MED':'Medina', 'MUX':'Multan',
                'MCT':'Muscat', 'PEW':'Peshawar', 'RYK':'Rahim Yar Khan',
                'UET':'Quetta', 'RUH':'Riyadh', 'SHJ':'Sharjah',
                'SKT':'Sialkot'}
    print('Input airport (AUH,DXB,...) or help')
    while True:
        airport = input(prompt)
        for ap in airports:
            if airport.upper().strip() == ap:
                return ap
        if airport.lower() == 'help':
            for ap in airports:
                print(ap,':',airports[ap])
                continue
        print("Airport is invalid.")


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

    # with open('Answer.html', 'w') as file:
    #     file.write(otvet)

    doc = lxml.html.document_fromstring(otvet)
    return doc


def get_info_from_doc(doc, depart_date, roundtrip):
    flights = []

    if roundtrip:
        rtrp = '2'
    else:
        rtrp = '1'
    depart_date = depart_date.replace('-', '_')
    flights_counter = 1
    while True:
        flight_info = {}
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
                        '//*[@id="trip_{}_date_{}"]/thead/tr[2]/th[{}]/span/text()'.format(
                            rtrp,
                            depart_date, k))[0]
                    coast = \
                        doc.xpath('{}[{}]/label/span/text()'.format(xpath_base,
                                                                    k + 1))[0]
                    currency = doc.xpath(
                        '{}[{}]/label/span/b/text()'.format(xpath_base, k + 1))[
                        0]
                    flight_type[flight_class] = str(coast + " " + currency)
                    k += 1
                except IndexError:
                    break
            flight_info["depart_date"] = (depart_date)
            flight_info['flight'] = (flight)
            depart_time = datetime.strptime(depart.lower(), '%I:%M %p')
            flight_info['depart_time'] = (
                datetime.strftime(depart_time, '%H:%M'))
            arrive_time = datetime.strptime(arrive.lower(), '%I:%M %p')
            flight_info['arrive_time'] = (
                datetime.strftime(arrive_time, '%H:%M'))
            time_in_flight = arrive_time - depart_time
            h_in_flight = time_in_flight.seconds // 3600
            m_in_flight = (time_in_flight.seconds // 60) % 60
            flight_info['time_in_flight'] = (
                '{}h {}m'.format(h_in_flight, m_in_flight))

            for ft in flight_type:
                flight_info[ft] = (flight_type[ft])
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


def print_flights(mass_flights):
    max_len = 0
    sep = str('-' * 20) + '+'
    exclusive_keys = []
    forward_flights = mass_flights[0]
    if len(mass_flights) == 2:
        back_flights = mass_flights[1]
    else:
        back_flights = []
    for k in mass_flights:
        for i in k:
            if len(i) >= max_len:
                max_len = len(i)
    header = ['Direction', 'Date', 'Flight', 'Depart Time', 'Arrive Time',
              'Time in air']
    sequence = ["depart_date", 'flight', 'depart_time', 'arrive_time',
                'time_in_flight']

    for i in forward_flights:
        for key in i:
            if key not in sequence and key not in exclusive_keys:
                exclusive_keys.append(key)
    for flight in back_flights:
        for key in flight:
            if key not in sequence and key not in exclusive_keys:
                exclusive_keys.append(key)

    for i in header:
        print("{:^20}".format(i), end='|')
    for i in exclusive_keys:
        print("{:^20}".format(i), end='|')
    print()
    print(sep * (len(header) + len(exclusive_keys)))
    for fl in forward_flights:
        print("{:^20}".format('Forward'), end='|')
        for key in fl:
            if key in sequence:
                print("{:^20}".format(fl[key]), end='|')
        for ex_key in exclusive_keys:
            if ex_key in fl.keys():
                print("{:^20}".format(fl[ex_key]), end='|')
            else:
                print(' '*20,end='|')
        print()
    if len(mass_flights) == 2:
        print(sep * (len(header) + len(exclusive_keys)))
        for flight in back_flights:
            print("{:^20}".format('Back'), end='|')
            for key in flight:
                if key in sequence:
                    print("{:^20}".format(flight[key]), end='|')
            for ex_key in exclusive_keys:
                if ex_key in flight.keys():
                    print("{:^20}".format(flight[ex_key]), end='|')
                else:
                    print(' '*20,end='|')
            print()


if __name__ == '__main__':
    departure = airport_input('Departure:')
    arrive = airport_input('Destination:')
    while True:
        depart_date = input_date('Date of flight out YYYY MM DD or today')
        if depart_date:
            break
        else:
            print("Depart date can't be empty")
    back_date = input_date('Date to return back or empty')
    back_date_flag = True
    if back_date is None:
        back_date_flag = False
        dep_date_datetime = create_date(depart_date)
        back_date = dep_date_datetime + timedelta(days=1)
        back_date = '{}-{:0>2}-{:0>2}'.format(back_date.year, back_date.month,
                                              back_date.day)

    my_params = {'AM': str(depart_date[:7]), 'AD': str(depart_date[8:]),
                 'RM': str(back_date[:7]), 'RD': str(back_date[8:]),
                 'DC': departure, 'AC': arrive}

    try:
        doc = get_document_from_site(my_params)
    except Exception:
        print('Some problems with site...')
        print(sys.exc_info()[1])
        exit(-1)

    forward_flights = get_info_from_doc(doc, depart_date, False)
    number_forward_flights = len(forward_flights)
    all_flights = [forward_flights]
    if back_date_flag:
        back_flights = get_info_from_doc(doc, back_date, True)
        all_flights.append(back_flights)

    print_flights(all_flights)