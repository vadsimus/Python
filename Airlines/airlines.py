"""
This module gets information about flights from www.airblue.com
"""
import sys
from datetime import datetime, date, timedelta
from itertools import product
from collections import namedtuple
import sqlite3
import lxml.html
import requests

AIRPORTS = {'AUH': 'Abu Dhabi', 'DXB': 'Dubai', 'DMM': 'Dammam',
            'ISB': 'Islmabad', 'JED': 'Jeddah', 'KHI': 'Karachi',
            'LHE': 'Lahore', 'MED': 'Medina', 'MUX': 'Multan',
            'MCT': 'Muscat', 'PEW': 'Peshawar', 'RYK': 'Rahim Yar Khan',
            'UET': 'Quetta', 'RUH': 'Riyadh', 'SHJ': 'Sharjah',
            'SKT': 'Sialkot'}

Flight = namedtuple(
    'Flight', ['depart_datetime', 'arrive_datetime',
               'departure_airport', 'arrive_airport',
               'flight', 'type_flight', 'cost', 'currency'])


def get_params_commandline():
    """returns data from command line if exists"""
    if 3 > len(sys.argv) > 5 or \
            sys.argv[1].upper() not in AIRPORTS or \
            sys.argv[2].upper() not in AIRPORTS:
        raise IndexError
    departure = sys.argv[1].upper()
    arrive = sys.argv[2].upper()
    depart_date = date.fromisoformat(sys.argv[3])
    try:
        back_date = date.fromisoformat(sys.argv[4])
        if back_date < depart_date:
            print('Back date can\'t be before depart date')
            print('One way search:')
            raise IndexError
    except IndexError:
        back_date = None
    return departure, arrive, depart_date, back_date


def input_dates():
    """returns dates inputed by user"""
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
    """returns irport inputed by user"""
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
            print("Airport input is invalid.")


def get_document_from_site(departure, arrive, depart_date, back_date=None):
    """returns answer from website"""
    my_url = "https://www.airblue.com/bookings/flight_selection.aspx?"
    my_params = {'FL': 'on', 'CC': 'Y', 'CD': '',
                 'PA': '1', 'PC': '', 'PI': '', 'x': '40', 'y': '20',
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
    """gettig base data from tbody"""
    Base_info = namedtuple('Base_info', ['flight', 'depart_time',
                                         'arrive_time'])
    flight = tbody[0].find_class('flight')[0].text.strip()
    depart_time = tbody[0].find_class('time leaving')[0].text
    depart_time = datetime.strptime('{}-{}'.format(
        search_date, depart_time.lower()), '%Y-%m-%d-%I:%M %p')
    arrive_time = tbody[0].find_class('time landing')[0].text
    arrive_time = datetime.strptime('{}-{}'.format(
        search_date, arrive_time.lower()), '%Y-%m-%d-%I:%M %p')
    if arrive_time < depart_time:
        arrive_time = arrive_time + timedelta(days=1)
    return Base_info(flight, depart_time, arrive_time)


def get_cost(tbody):
    """get flight_type, cost and currency from tbody"""
    result = []
    Costs = namedtuple('Costs', ['flight_type', 'cost', 'currency'])
    for flight_type in ['family-ED', 'family-ES']:
        try:
            cost = tbody[0].find_class(flight_type)[0].xpath(
                'label/span/text()')[0]
            cost = int(''.join(cost.split(',')))
            currency = tbody[0].find_class(flight_type)[0].xpath(
                'label/span/b/text()')[0]
            result.append(Costs(flight_type, cost, currency))
        except IndexError:
            pass
    return result


def get_info_from_doc(answer, departure_airport, arrive_airport,
                      depart_date, arrive_date):
    """parsing answer from website"""
    result = []
    for i, table in enumerate(lxml.html.fromstring(answer).xpath(
            "//table[contains(@class,'requested-date')]")):
        for tbody in table.findall('tbody'):
            try:
                base_data = get_base_flight_data(tbody, depart_date if i == 0
                                                 else arrive_date)
            except IndexError:
                continue
            cost_data = get_cost(tbody)
            for cost in cost_data:
                result.append(Flight(
                    base_data.depart_time, base_data.arrive_time,
                    departure_airport if i == 0 else arrive_airport,
                    arrive_airport if i == 0 else departure_airport,
                    base_data.flight,
                    'Standard (1 Bag)' if cost.flight_type == 'family-ES'
                    else 'Discount (No Bags)',
                    cost.cost, cost.currency
                ))
    return result


def divide_flights(all_flights, departure):
    """devide all flights to forward and back directions"""
    forward_flights = []
    back_flights = []
    for i in all_flights:
        if i.departure_airport == departure:
            forward_flights.append(i)
        else:
            back_flights.append(i)
    return forward_flights, back_flights


def print_flight(flight):
    """print all info from flight"""
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
          f'{flight.cost} {flight.currency}')


def print_all_flights(forward_flights, back_flights, back_date):
    """print all flights sorted by cost"""
    if not back_date:
        print('The following flights were found:' if forward_flights
              else 'No fights found.')
        forward_flights.sort(key=lambda fl: fl.cost)
        for index, flight in enumerate(forward_flights):
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


def create_table(crs):
    """create table in database if not exists"""
    crs.execute("create table if not exists flights ("
                "'roundtrip' int,"
                "'departdt' string(30),"
                "'arrivedt' string(30),"
                "'depart' string(3), 'arrive' string(3),"
                "'flight' string(10),"
                "'typeflight' string(15), 'cost' int,"
                "'currency' string(3))")


def add_flights_to_db(crs, forward_flights, back_flights, params):
    """add flight info to database"""
    rtrp = 1 if params.back_date else 0
    for flights in (forward_flights, back_flights):
        for flight in flights:
            cur = crs.execute('select * from flights where roundtrip = ? and '
                              'depart = ? and arrive = ? and flight = ? and '
                              'typeflight = ? and departdt like ?',
                              [rtrp, flight.departure_airport,
                               flight.arrive_airport,
                               flight.flight, flight.type_flight,
                               str(flight.depart_datetime.date()) + '%'])
            if len(cur.fetchall()) == 0:
                crs.execute('insert or ignore into flights values'
                            '(?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            [rtrp, *flight])


def get_flights_from_db(crs, params):
    """get flights info from database"""
    frmt = '%Y-%m-%d %H:%M:%S'
    rtrp = 1 if params.back_date else 0
    result = []
    for i, search_date in enumerate((params.depart_date, params.back_date)):
        cur = crs.execute('select * from flights where roundtrip = ? and '
                          'depart = ? and arrive = ? and departdt like ?',
                          [rtrp, params.departure if i == 0 else params.arrive,
                           params.arrive if i == 0 else params.departure,
                           str(search_date) + '%'])
        for k in cur.fetchall():
            result.append(Flight(datetime.strptime(k[1], frmt),
                                 datetime.strptime(k[2], frmt),
                                 k[3], k[4], k[5], k[6], k[7],
                                 k[8]))
    return result


def main():
    """Main function"""
    try:
        departure, arrive, depart_date, back_date = get_params_commandline()
    except (IndexError, ValueError):
        print('Params are not valid')
        departure = airport_input('Departure:')
        arrive = airport_input('Destination:')
        depart_date, back_date = input_dates()
    Params = namedtuple('Params',
                        ['departure', 'arrive', 'depart_date', 'back_date'])
    params = Params(departure, arrive, depart_date, back_date)
    conn = sqlite3.connect('flights.db')
    crs = conn.cursor()
    create_table(crs)
    all_flights = get_flights_from_db(crs, params)
    forward_flights, back_flights = divide_flights(all_flights, departure)
    if not forward_flights or not all([back_date, back_flights]):
        answer = get_document_from_site(*params)
        all_flights = get_info_from_doc(answer.content, *params)
        forward_flights, back_flights = divide_flights(all_flights, departure)
        add_flights_to_db(crs, forward_flights, back_flights, params)
    else:
        print('Info from local database')
    print_all_flights(forward_flights, back_flights, back_date)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
