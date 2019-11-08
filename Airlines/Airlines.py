from urllib import request, parse
import sys
import re
import lxml.html
from datetime import datetime
import json
from itertools import product


def create_date(string):
    try:
        dt = datetime.strptime(string, '%d-%m-%y')
        return dt
    except ValueError or TypeError:
        return None


def input_date(direction):
    if direction == "Forward":
        prompt = 'Date of flight out {DD MM YY}:'
    elif direction == "Back":
        prompt = 'Date to return back {DD MM YY} or empty:'
    today = datetime.now()
    while True:
        date = list(re.split('[ \-_]', input(prompt)))
        if date[0].strip() == '' and direction == 'Back':
            return None
        elif date[0].strip() == '' and direction == 'Forward':
            print("Depart date can't be empty!")
            continue
        elif create_date('-'.join(date)):
            d = create_date('-'.join(date))
            if d.year == today.year and d.month == today.month and d.day == today.day:
                return d
            elif d < today:
                print("Date can't be in past. Today is {}-{}-{}".format(
                    today.day, today.month, today.year))
                continue
            return d
        else:
            print('Wrong!!!')


def airport_input(prompt):
    airports = {'AUH': 'Abu Dhabi', 'DXB': 'Dubai', 'DMM': 'Dammam',
                'ISB': 'Islmabad', 'JED': 'Jeddah', 'KHI': 'Karachi',
                'LHE': 'Lahore', 'MED': 'Medina', 'MUX': 'Multan',
                'MCT': 'Muscat', 'PEW': 'Peshawar', 'RYK': 'Rahim Yar Khan',
                'UET': 'Quetta', 'RUH': 'Riyadh', 'SHJ': 'Sharjah',
                'SKT': 'Sialkot'}
    print('Input airport (AUH,DXB,...) or help')
    while True:
        airport = input(prompt).upper().strip()
        if airport in airports.keys():
            print(airports[airport])
            return airport
        if airport == 'HELP':
            for ap in airports:
                print(ap, ':', airports[ap])
                continue
        print("Airport input is invalid.")


def get_document_from_site(my_params, b_flag):
    myUrl = "https://www.airblue.com/bookings/flight_selection.aspx?"
    value = {'TT': 'OW', 'FL': 'on', 'CC': 'Y', 'CD': '',
             'PA': '1', 'PC': '', 'PI': '', 'x': '40', 'y': '20',
             'AD': my_params['AD'],
             'AM': my_params['AM'],
             'DC': my_params['DC'],
             'AC': my_params['AC']
             }
    if b_flag:
        value['TT'] = 'RT'
        value['RD'] = my_params['RD']
        value['RM'] = my_params['RM']
    mydata = parse.urlencode(value)
    myUrl = myUrl + mydata
    req = request.Request(myUrl)
    answer = request.urlopen(req)
    answer = answer.read().decode('UTF-8')
    document = lxml.html.document_fromstring(answer)
    return document


def get_info_from_doc(doc, depart_date, roundtrip):
    flights = []
    if roundtrip:
        rtrp = '2'
    else:
        rtrp = '1'
    flights_counter = 1
    while True:
        flight_info = {}
        try:
            xpath_base = '//*[@id="trip_{}_date_{}"]/tbody[{}]/tr/td'
            xpath_base = xpath_base.format(rtrp, depart_date, flights_counter)
            flight = doc.xpath('{}[1]/text()'.format(xpath_base))[0].strip()
            depart = doc.xpath('{}[2]/text()'.format(xpath_base))[0]
            arrive = doc.xpath('{}[4]/text()'.format(xpath_base))[0]
            flight_type = {}
            for k in range(5, 7):
                try:
                    flight_class = doc.xpath(
                        '//*[@id="trip_{}_date_{}"]/thead/tr[2]/th[{}]/span/text()'.format(
                            rtrp, depart_date, k))[0]
                    cost = \
                        doc.xpath('{}[{}]/label/span/text()'.format(xpath_base,
                                                                    k + 1))[0]
                    currency = doc.xpath(
                        '{}[{}]/label/span/b/text()'.format(
                            xpath_base, k + 1))[0]
                    flight_type[flight_class] = str(cost + " " + currency)
                except Exception:
                    pass

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
            flight_info['time_in_flight'] = '{}h {}m'.format(
                h_in_flight, m_in_flight)
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
    def print_headers(header, exclusive):
        print('┌' + ('─' * 20 + '┬') * (len(header) +
                                        len(exclusive) - 1) + (
                      '─' * 20 + '┐'))
        print('│', end='')
        for i in header:
            print("{:^20}".format(i), end='│')
        for i in exclusive:
            print("{:^20}".format(i), end='│')
        print()

    def print_separator(len_table):
        print(
            '├' + sep * (len_table - 1) + (
                    '─' * 20 + '┤'))

    def print_flights_to_table(fl, direction, sequence, exclusive_keys):
        print('│', end='')
        print("{:^20}".format(direction), end='|')
        for key in fl:
            if key in sequence:
                print("{:^20}".format(fl[key]), end='|')
        for ex_key in exclusive_keys:
            if ex_key in fl.keys():
                print("{:^20}".format(fl[ex_key]), end='|')
            else:
                print(' ' * 20, end='|')
        print()

    def print_end_table(len_table):
        print('└' + ('─' * 20 + '┴') * (len_table - 1) + (
                '─' * 20 + '┘'))

    max_len = 0
    sep = str('─' * 20) + '┼'
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
    for flight in forward_flights:
        for key in flight:
            if key not in sequence and key not in exclusive_keys:
                exclusive_keys.append(key)
    for flight in back_flights:
        for key in flight:
            if key not in sequence and key not in exclusive_keys:
                exclusive_keys.append(key)
    if 'Discount (No Bags)' in exclusive_keys:
        exclusive_keys.append('Cost Trip Discount')
    if 'Standard (1 Bag)' in exclusive_keys:
        exclusive_keys.append('Cost Trip Standart')

    len_table = len(header) + len(exclusive_keys)
    if len(mass_flights) == 1:
        print_headers(header, exclusive_keys)
        print_separator(len_table)
        print_flights_to_table(forward_flights, 'Forward', sequence,
                               exclusive_keys)
        print_end_table(len_table)
    else:
        comb = list(product(forward_flights, back_flights))

        print_headers(header, exclusive_keys)
        for i in comb:
            if i[0]['depart_date'] != i[1]['depart_date'] or \
                    i[0]['arrive_time'] < i[1]['depart_time']:

                print_separator(len_table)
                print_flights_to_table(i[0], 'Forward', sequence,
                                       exclusive_keys)
                if 'Standard (1 Bag)' in exclusive_keys:
                    try:
                        fl1_cost, fl1_cop = i[0]['Standard (1 Bag)'].split()
                        fl2_cost, fl2_cop = i[1]['Standard (1 Bag)'].split()
                        if fl1_cop == fl2_cop:
                            trip_cost = float(fl1_cost.replace(',', '.')) + float(fl2_cost.replace(',', '.'))

                            i[1]['Cost Trip Standart'] = str(trip_cost).replace('.',',') + ' ' + fl1_cop
                    except Exception as e:
                        pass
                if 'Discount (No Bags)' in exclusive_keys:
                    try:
                        fl1_cost, fl1_cop = i[0]['Discount (No Bags)'].split()
                        fl2_cost, fl2_cop = i[1]['Discount (No Bags)'].split()
                        if fl1_cop == fl2_cop:
                            trip_cost = float(fl1_cost.replace(',', '.')) + float(
                                fl2_cost.replace(',', '.'))

                            i[1]['Cost Trip Discount'] = str(trip_cost).replace('.',',') + ' ' + fl1_cop
                    except Exception as e:
                        pass
                print_flights_to_table(i[1], 'Back', sequence,
                                       exclusive_keys)
        print_end_table(len_table)

        # print_headers(header, exclusive_keys)
        # print_separator(len_table)
        # print_flights_to_table(forward_flights, 'Forward', sequence, exclusive_keys)
        # print_separator(len_table)
        # print_flights_to_table(back_flights, 'Back', sequence, exclusive_keys)
        # print_end_table(len_table)


if __name__ == '__main__':
    departure = airport_input('Departure:')
    arrive = airport_input('Destination:')
    depart_date = input_date('Forward')
    back_date = input_date('Back')
    back_flag = True
    if back_date is None or back_date < depart_date:
        if back_date:
            print("Back date can't be before depart date.")
        back_flag = False
        back_date = depart_date

    my_params = {
        'AM': '{:0>4}-{:0>2}'.format(depart_date.year, depart_date.month),
        'AD': '{:0>2}'.format(depart_date.day),
        'DC': departure, 'AC': arrive
    }
    if back_flag:
        my_params['RM'] = '{:0>4}-{:0>2}'.format(back_date.year,
                                                 back_date.month)
        my_params['RD'] = '{:0>2}'.format(back_date.day)
    try:
        doc = get_document_from_site(my_params, back_flag)
    except Exception as ex:
        print('Some problems with site...')
        print(sys.exc_info()[1])
        exit(-1)

    if back_flag:
        forward_flights = get_info_from_doc(doc, '{:0>4}_{:0>2}_{:0>2}'.format(
            depart_date.year, depart_date.month, depart_date.day), False)
        all_flights = [forward_flights]
        back_flights = get_info_from_doc(doc, '{:0>4}_{:0>2}_{:0>2}'.format(
            back_date.year, back_date.month, back_date.day), True)
        all_flights.append(back_flights)
    else:
        forward_flights = get_info_from_doc(doc, '{:0>4}_{:0>2}_{:0>2}'.format(
            depart_date.year, depart_date.month, depart_date.day), False)
        all_flights = [forward_flights]
    with open('flight3.dat', 'w') as file:
        json.dump(all_flights, file)

    print_flights(all_flights)
