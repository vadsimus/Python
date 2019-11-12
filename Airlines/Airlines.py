from urllib import request, parse
import sys
import re
import lxml.html
from datetime import datetime
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
            # If compare entered datetime and today, entered date will be in past
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
    depart_date = '{:0>4}_{:0>2}_{:0>2}'.format(
        depart_date.year, depart_date.month, depart_date.day)
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
                except IndexError:
                    pass

            flight_info["depart_date"] = depart_date
            flight_info['flight'] = flight
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
                pass
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
        sep = str('─' * 20) + '┼'
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

    def sum_flight_cost(cost1, cost2):
        fl1_cost, fl1_currency = cost1.split()
        fl1_cost = int(''.join(fl1_cost.split(',')))
        fl2_cost, fl2_currency = cost2.split()
        fl2_cost = int(''.join(fl2_cost.split(',')))
        trip_cost = (fl1_cost + fl2_cost)
        if len(str(trip_cost)) > 3:
            s_trip_cost = '{:,}'.format(trip_cost)
        else:
            s_trip_cost = str(trip_cost)
        return s_trip_cost + ' ' + fl1_currency

    exclusive_keys = []
    forward_flights = mass_flights[0]
    if len(mass_flights) == 2:
        back_flights = mass_flights[1]
    else:
        back_flights = []
    header = ['Direction', 'Date', 'Flight', 'Depart Time', 'Arrive Time',
              'Time in air']
    sequence = ["depart_date", 'flight', 'depart_time', 'arrive_time',
                'time_in_flight']
    for flights in forward_flights, back_flights:
        for flight in flights:
            for key in flight:
                if key not in sequence and key not in exclusive_keys:
                    exclusive_keys.append(key)
    if len(mass_flights) == 2:
        if 'Discount (No Bags)' in exclusive_keys or \
                'Standard (1 Bag)' in exclusive_keys:
            exclusive_keys.append('Round Trip Cost')
        if 'Discount (No Bags)' in exclusive_keys and \
                'Standard (1 Bag)' in exclusive_keys:
            exclusive_keys.append('Trip Combinations')
    len_table = len(header) + len(exclusive_keys)
    print_headers(header, exclusive_keys)
    if len(mass_flights) == 1:
        print_separator(len_table)
        for flight in forward_flights:
            print_flights_to_table(flight, 'Forward', sequence,
                                   exclusive_keys)
    else:
        comb = list(product(forward_flights, back_flights))
        for i in comb:
            if i[0]['depart_date'] != i[1]['depart_date'] or \
                    i[0]['arrive_time'] < i[1]['depart_time']:
                print_separator(len_table)
                if 'Standard (1 Bag)' in exclusive_keys:
                    try:
                        i[0]['Round Trip Cost'] = 'St: ' + sum_flight_cost(
                            i[0]['Standard (1 Bag)'],
                            i[1]['Standard (1 Bag)']
                        )
                    except KeyError:
                        pass
                if 'Discount (No Bags)' in exclusive_keys:
                    try:
                        i[1]['Round Trip Cost'] = 'Dis: ' + sum_flight_cost(
                            i[0]['Discount (No Bags)'],
                            i[1]['Discount (No Bags)']
                        )
                    except KeyError:
                        pass
                if 'Standard (1 Bag)' in exclusive_keys and \
                        'Discount (No Bags)' in exclusive_keys:
                    try:
                        i[0]['Trip Combinations'] = 'St-Dis: ' + sum_flight_cost(
                            i[0]['Standard (1 Bag)'],
                            i[1]['Discount (No Bags)']
                        )
                    except KeyError:
                        pass
                    try:
                        i[1]['Trip Combinations'] = 'Dis-St: ' + sum_flight_cost(
                            i[0]['Discount (No Bags)'],
                            i[1]['Standard (1 Bag)']
                        )
                    except KeyError:
                        pass
                print_flights_to_table(i[0], 'Forward', sequence,
                                       exclusive_keys)
                print_flights_to_table(i[1], 'Back', sequence,
                                       exclusive_keys)
    print_end_table(len_table)


if __name__ == '__main__':
    departure = airport_input('Departure:')
    arrive = airport_input('Destination:')
    depart_date = input_date('Forward')
    back_date = input_date('Back')
    if back_date is None or back_date < depart_date:
        if back_date:
            print(
                "Back date can't be before forward depart date. One way trip is shown.")
        back_flag = False
    else:
        back_flag = True
    my_params = {
        'AM': '{:0>4}-{:0>2}'.format(depart_date.year, depart_date.month),
        'AD': '{:0>2}'.format(depart_date.day),
        'DC': departure, 'AC': arrive}
    if back_flag:
        my_params['RM'] = '{:0>4}-{:0>2}'.format(back_date.year,
                                                 back_date.month)
        my_params['RD'] = '{:0>2}'.format(back_date.day)
    try:
        doc = get_document_from_site(my_params, back_flag)
    except Exception as ex:
        print('Some problems with website...')
        print(sys.exc_info()[1])
        exit(-1)
    if back_flag:
        forward_flights = get_info_from_doc(doc, depart_date, False)
        all_flights = [forward_flights]
        back_flights = get_info_from_doc(doc, back_date, True)
        all_flights.append(back_flights)
    else:
        forward_flights = get_info_from_doc(doc, depart_date, False)
        all_flights = [forward_flights]

    print_flights(all_flights)