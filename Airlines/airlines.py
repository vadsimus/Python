'''
This module receives flight information from www.airblue.com
'''
import sys
from datetime import datetime, date, timedelta
from itertools import product
from collections import namedtuple
import argparse
import lxml.html
import requests

AIRPORTS = {'AUH': 'Abu Dhabi', 'DXB': 'Dubai', 'DMM': 'Dammam',
            'ISB': 'Islmabad', 'JED': 'Jeddah', 'KHI': 'Karachi',
            'LHE': 'Lahore', 'MED': 'Medina', 'MUX': 'Multan',
            'MCT': 'Muscat', 'PEW': 'Peshawar', 'RYK': 'Rahim Yar Khan',
            'UET': 'Quetta', 'RUH': 'Riyadh', 'SHJ': 'Sharjah',
            'SKT': 'Sialkot'}


def get_params_commandline():
    '''returns data from command line if exists.
    Can raise IndexError if wrong airport or ValueError if wrong dates'''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'depart', nargs='?', help='depart airport', default=None)
    parser.add_argument(
        'arrive', nargs='?', help='arrive airport', default=None)
    parser.add_argument('depart_date', nargs='?',
                        help='departure date', default=None)
    parser.add_argument('back_date', nargs='?',
                        help='back date', default=None)
    args = parser.parse_args()
    if args.depart.upper() not in AIRPORTS or \
            args.arrive.upper() not in AIRPORTS:
        raise IndexError
    if not args.depart_date:
        raise ValueError
    depart_date = date.fromisoformat(args.depart_date)
    if args.back_date:
        back_date = date.fromisoformat(args.back_date)
        if back_date < depart_date:
            print('Back date can\'t be before depart date')
            raise IndexError
    else:
        back_date = None
    return args.depart.upper(), args.arrive.upper(), \
           depart_date, back_date


def input_dates():
    '''returns dates entered by user'''
    while True:
        f_out = input('Date of flight out {YYYY-MM-DD}:')
        f_back = input('Date to return back {YYYY-MM-DD} or empty:')
        if f_out == '':
            print('Depart date can\'t be empty!')
            continue
        try:
            dt_f_out = date.fromisoformat(f_out)
            if f_back.strip():
                dt_f_back = date.fromisoformat(f_back)
            else:
                dt_f_back = None
        except ValueError:
            print('Wrong format, try once else..')
            continue
        if dt_f_out < date.today():
            print(
                f'Date can\'t be in past. Today is {date.today().isoformat()}')
            continue
        if dt_f_back and dt_f_back < dt_f_out:
            print('Back date can\'t be before depart date')
            continue
        return dt_f_out, dt_f_back


def airport_input(prompt):
    '''returns airport inputed by user'''
    print('Input airport (AUH,DXB,...) or help')
    while True:
        airport = input(prompt).upper().strip()
        if airport in AIRPORTS:
            print(AIRPORTS[airport])
            return airport
        if airport == 'HELP':
            for code, name in AIRPORTS.items():
                print(code, ':', name)
        else:
            print('Airport input is invalid.')


def get_document_from_site(departure, arrive, depart_date, back_date=None):
    '''returns answer from website'''
    my_url = 'https://www.airblue.com/bookings/flight_selection.aspx'
    my_params = {'PA': '1',
                 'AM': '{:0>4}-{:0>2}'.format(depart_date.year,
                                              depart_date.month),
                 'AD': '{:0>2}'.format(depart_date.day),
                 'DC': departure, 'AC': arrive, 'TT': 'OW'}
    if back_date:
        my_params.update({
            'RM': '{:0>4}-{:0>2}'.format(back_date.year, back_date.month),
            'RD': '{:0>2}'.format(back_date.day),
            'TT': 'RT'
        })
    try:
        answer = requests.get(my_url, params=my_params)
    except requests.exceptions.RequestException:
        print('Some problems with network or website')
        sys.exit(-1)
    if answer.status_code != 200:
        print(f'Some problems with site, code:{answer.status_code}')
        sys.exit(-1)
    return answer


def get_base_flight_data(tbody, search_date):
    '''gets base data from tbody'''
    Base_info = namedtuple('Base_info', ['flight', 'depart_time',
                                         'arrive_time'])
    flight = tbody[0].find_class('flight')[0].text.strip()
    depart_time = tbody[0].find_class('time leaving')[0].text
    depart_time = datetime.strptime(str(search_date) + '-' +
                                    depart_time.lower(), '%Y-%m-%d-%I:%M %p')
    arrive_time = tbody[0].find_class('time landing')[0].text
    arrive_time = datetime.strptime(str(search_date) + '-' +
                                    arrive_time.lower(), '%Y-%m-%d-%I:%M %p')
    if arrive_time < depart_time:
        arrive_time = arrive_time + timedelta(days=1)
    return Base_info(flight, depart_time, arrive_time)


def get_cost(tbody, thead):
    '''gets flight_type, cost and currency from tbody'''
    result = []
    Costs = namedtuple('Costs', ['flight_type', 'cost', 'currency'])
    for tbody_td in tbody[0].find_class('family'):
        try:
            flight_type = thead.find_class(
                tbody_td.xpath('@class')[0].split()[1])[0].xpath(
                    'span/text()')[0]
            cost = tbody_td.xpath('label/span/text()')[0]
            cost = float(cost.replace(',', ''))
            currency = tbody_td.xpath('label/span/b/text()')[0]
            result.append(Costs(flight_type, cost, currency))
        except IndexError:
            continue
    return result


def get_info_from_doc(answer, departure_airport, arrive_airport,
                      depart_date, arrive_date):
    '''parsing the response from the site'''
    Flight = namedtuple(
        'Flight', ['depart_datetime', 'arrive_datetime',
                   'departure_airport', 'arrive_airport', 'flight',
                   'type_flight', 'cost', 'currency'])
    result = []
    for is_outbound, table in enumerate(lxml.html.fromstring(answer).xpath(
            '//table[contains(@class,"requested-date")]')):
        flights = []
        for tbody in table.findall('tbody'):
            try:
                base_data = get_base_flight_data(
                    tbody, depart_date if is_outbound == 0 else arrive_date)
            except IndexError:
                continue
            cost_data = get_cost(tbody, table.findall('thead')[0])
            for cost in cost_data:
                flights.append(Flight(
                    base_data.depart_time, base_data.arrive_time,
                    departure_airport if is_outbound == 0 else arrive_airport,
                    arrive_airport if is_outbound == 0 else departure_airport,
                    base_data.flight,
                    cost.flight_type,
                    cost.cost, cost.currency
                ))
        result.append(flights)
    return result


def print_flight(flight):
    '''print all flight information'''
    format_dt = '%Y-%m-%d %H:%M'
    time_in_flight = flight.arrive_datetime - flight.depart_datetime
    h_in_flight = time_in_flight.seconds // 3600
    m_in_flight = (time_in_flight.seconds // 60) % 60
    time_in_flight = '{}h {}m'.format(h_in_flight, m_in_flight)
    print(f'{flight.departure_airport}-{flight.arrive_airport}:'
          f'{flight.flight} '
          f'{flight.depart_datetime.strftime(format_dt)} - '
          f'{flight.arrive_datetime.strftime(format_dt)} '
          f'({time_in_flight}) {flight.type_flight} '
          f'{int(flight.cost) if flight.cost.is_integer() else flight.cost} '
          f'{flight.currency}')


def print_all_flights(back_date, forward_flights, back_flights=None):
    '''print all flights sorted by cost'''
    if not back_date:
        print('The following flights were found:' if forward_flights
              else 'No fights found.')
        forward_flights.sort(key=lambda fl: fl.cost)
        for index, flight in enumerate(sorted(forward_flights,
                                              key=lambda fl: fl.cost)):
            print(f'{index + 1}) ', end='')
            print_flight(flight)
    else:
        combinations = []
        for comb in product(forward_flights, back_flights):
            if comb[0].arrive_datetime < comb[1].depart_datetime:
                combinations.append(comb)
        combinations.sort(key=lambda x: x[0].cost + x[1].cost)
        print('The following flight combinations were found:' if combinations
              else 'No flight combinations found.')
        for index, i in enumerate(combinations):
            if i[0].arrive_datetime < i[1].depart_datetime:
                print(f'{index + 1})', end='')
                print_flight(i[0])
                print('  ', end='')
                print_flight(i[1])
                print(
                    f'  Total price: {i[0].cost + i[1].cost} '
                    f'{i[0].currency}')


def main():
    '''Main function'''
    try:
        departure, arrive, depart_date, back_date = get_params_commandline()
    except (IndexError, ValueError):
        print('Params are not valid')
        departure = airport_input('Departure:')
        arrive = airport_input('Destination:')
        depart_date, back_date = input_dates()
    answer = get_document_from_site(departure, arrive, depart_date, back_date)
    all_flights = get_info_from_doc(answer.content, departure, arrive,
                                    depart_date, back_date)
    print_all_flights(back_date, *all_flights)


if __name__ == '__main__':
    main()
