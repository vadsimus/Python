"""
This module gets information about flights from www.airblue.com
"""
import sys
from datetime import datetime, date, timedelta
from itertools import product
from collections import namedtuple
import lxml.html
import requests

AIRPORTS = {'AUH': 'Abu Dhabi', 'DXB': 'Dubai', 'DMM': 'Dammam',
            'ISB': 'Islmabad', 'JED': 'Jeddah', 'KHI': 'Karachi',
            'LHE': 'Lahore', 'MED': 'Medina', 'MUX': 'Multan',
            'MCT': 'Muscat', 'PEW': 'Peshawar', 'RYK': 'Rahim Yar Khan',
            'UET': 'Quetta', 'RUH': 'Riyadh', 'SHJ': 'Sharjah',
            'SKT': 'Sialkot'}


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




def get_info_from_doc(answer, departure_airport, arrive_airport,
                      depart_date, back_date):
    """parsing answer from website"""
    result = []
    htmltree = lxml.html.document_fromstring(answer.content)
    dates = [depart_date]
    if back_date:
        dates.append(back_date)
    for i, search_date in enumerate(dates):
        search_date = '{:0>4}_{:0>2}_{:0>2}'.format(
            search_date.year, search_date.month, search_date.day)
        xpath_table = '//*[@id="trip_{}_date_{}"]'.format(
            i + 1, search_date)
        for flights_counter in range(
                1, len(htmltree.xpath(xpath_table)[0].getchildren()) - 1):
            xpath_base = '//*[@id="trip_{}_date_{}"]/tbody[{}]/tr/td'
            xpath_base = xpath_base.format(i + 1, search_date,
                                           flights_counter)
            flight_type = {}
            try:
                flight = htmltree.xpath('{}[1]/text()'.format(xpath_base))[
                    0].strip()
                depart = htmltree.xpath('{}[2]/text()'.format(xpath_base))[0]
                arrive = htmltree.xpath('{}[4]/text()'.format(xpath_base))[0]
                for k in range(5, 7):
                    try:
                        flight_class = htmltree.xpath(
                            xpath_table +
                            '/thead/tr[2]/th[{}]/span/text()'.format(k))[0]
                        cost = htmltree.xpath(
                            '{}[{}]/label/span/text()'.format(xpath_base,
                                                              k + 1))[0]
                        currency = htmltree.xpath(
                            '{}[{}]/label/span/b/text()'.format(
                                xpath_base, k + 1))[0]
                        flight_type[flight_class] = str(cost + " " + currency)
                    except IndexError:
                        pass
            except IndexError:
                break
            try:
                depart_time = datetime.strptime('{}-{}'.format(
                    search_date, depart.lower()), '%Y_%m_%d-%I:%M %p')
                arrive_time = datetime.strptime('{}-{}'.format(
                    search_date, arrive.lower()), '%Y_%m_%d-%I:%M %p')
            except ValueError:
                break
            if arrive_time < depart_time:
                arrive_time = arrive_time + timedelta(days=1)
            time_in_flight = arrive_time - depart_time
            h_in_flight = time_in_flight.seconds // 3600
            m_in_flight = (time_in_flight.seconds // 60) % 60

            for key in ['Standard (1 Bag)', 'Discount (No Bags)']:
                if key in flight_type:
                    fl_cost, fl_currency = flight_type[key].split()
                    fl_cost = int(''.join(fl_cost.split(',')))
                    Flight = namedtuple(
                        'Flight', ['depart_datetime', 'arrive_datetime',
                                   'departure_airport', 'arrive_airport',
                                   'time_in_flight', 'flight',
                                   'type_flight', 'cost', 'currency'])
                    flight_instance = Flight(
                        depart_time, arrive_time,
                        departure_airport if i == 0 else arrive_airport,
                        arrive_airport if i == 0 else departure_airport,
                        '{}h {}m'.format(h_in_flight, m_in_flight),
                        flight, key, fl_cost, fl_currency)
                    result.append(flight_instance)

    return result


def print_flight(flight):
    """print all info from flight"""
    format_dt = '%Y-%m-%d %H:%M'
    print(f'{flight.departure_airport}-{flight.arrive_airport}:'
          f'{flight.flight} '
          f'{flight.depart_datetime.strftime(format_dt)} - '
          f'{flight.arrive_datetime.strftime(format_dt)} '
          f'({flight.time_in_flight}) {flight.type_flight} '
          f'{flight.cost} {flight.currency}')


def print_all_flights(all_flights, departure, back_date):
    """print all flights sorted by cost"""
    print('The following flights were found:')
    if not back_date:
        all_flights.sort(key=lambda fl: fl.cost)
        for index, flight in enumerate(all_flights):
            print(f'{index + 1}) ', end='')
            print_flight(flight)
    else:
        forward_flights = []
        back_flights = []
        for i in all_flights:
            if i.departure_airport == departure:
                forward_flights.append(i)
            else:
                back_flights.append(i)
        comb = list(product(forward_flights, back_flights))
        comb.sort(key=lambda x: x[0].cost + x[1].cost)
        index = 1
        for i in comb:
            if i[0].arrive_datetime < i[1].depart_datetime:
                print(f'{index})', end='')
                index += 1
                print_flight(i[0])
                print('  ', end='')
                print_flight(i[1])
                print(
                    f'  Total price: {i[0].cost + i[1].cost} '
                    f'{i[0].currency}')


def main():
    """Main function"""
    try:
        departure, arrive, depart_date, back_date = get_params_commandline()
    except (IndexError, ValueError):
        print('Params are not valid')
        departure = airport_input('Departure:')
        arrive = airport_input('Destination:')
        depart_date, back_date = input_dates()
    answer = get_document_from_site(departure, arrive, depart_date, back_date)
    all_flights = get_info_from_doc(answer, departure, arrive,
                                    depart_date, back_date, )
    print_all_flights(all_flights, departure, back_date)


if __name__ == "__main__":
    main()
