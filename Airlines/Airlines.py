from urllib import request, parse
import sys
import requests
from datetime import datetime, date, time, timedelta
import lxml.html
from itertools import product

airports = {'AUH': 'Abu Dhabi', 'DXB': 'Dubai', 'DMM': 'Dammam',
            'ISB': 'Islmabad', 'JED': 'Jeddah', 'KHI': 'Karachi',
            'LHE': 'Lahore', 'MED': 'Medina', 'MUX': 'Multan',
            'MCT': 'Muscat', 'PEW': 'Peshawar', 'RYK': 'Rahim Yar Khan',
            'UET': 'Quetta', 'RUH': 'Riyadh', 'SHJ': 'Sharjah',
            'SKT': 'Sialkot'}


class Flight:
    def __init__(self, depart_datetime,
                 arrive_datetime, depart_airport, arrirve_airport,
                 time_in_flight, flight, type_flight, cost, currency):
        self.depart_datetime = depart_datetime
        self.arrive_datetime = arrive_datetime
        self.depart_airport = depart_airport
        self.arrirve_airport = arrirve_airport
        self.flight = flight
        self.type_flight = type_flight
        self.cost = cost
        self.currency = currency
        self.time_in_flight = time_in_flight

    def __str__(self):
        return f'{self.depart_airport}-{self.arrirve_airport}: ' \
               f'{self.depart_datetime} - {self.arrive_datetime} ' \
               f'({self.time_in_flight}) {self.flight} ' \
               f'{self.type_flight} : {self.cost} {self.currency}'


def input_dates():
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
        if dt_f_out < date.today() or dt_f_back and dt_f_back < date.today():
            print(
                f'Date can\'t be in past. Today is {date.today().isoformat()}')
            continue
        elif dt_f_back and dt_f_back < dt_f_out:
            print('Back date can\'t be before depart date')
            continue
        else:
            return dt_f_out, dt_f_back


def airport_input(prompt):
    print('Input airport (AUH,DXB,...) or help')
    while True:
        airport = input(prompt).upper().strip()
        if airport in airports:
            print(airports[airport])
            return airport
        elif airport == 'HELP':
            for code, name in airports.items():
                print(code, ':', name)
        else:
            print("Airport input is invalid.")


def get_document_from_site(my_params):
    myUrl = "https://www.airblue.com/bookings/flight_selection.aspx?"
    my_params.update({'FL': 'on', 'CC': 'Y', 'CD': '',
                      'PA': '1', 'PC': '', 'PI': '', 'x': '40', 'y': '20', })
    answer = requests.get(myUrl, params=my_params)
    return answer


def get_info_from_doc(answer, depart_date, back_date, departure_airport,
                      arrive_airport):
    flights = []
    htmltree = lxml.html.document_fromstring(answer.content)
    dates = [depart_date]
    if back_date:
        dates.append(back_date)
    for rtrp, search_date in enumerate(dates):
        search_date = '{:0>4}_{:0>2}_{:0>2}'.format(
            search_date.year, search_date.month, search_date.day)
        x = htmltree.xpath('//*[@id="trip_{}_date_{}"]'.format(
            rtrp + 1, search_date))
        for flights_counter in range(1, len(x[0].getchildren()) - 1):
            try:
                xpath_base = '//*[@id="trip_{}_date_{}"]/tbody[{}]/tr/td'
                xpath_base = xpath_base.format(rtrp + 1, search_date,
                                               flights_counter)
                flight = htmltree.xpath('{}[1]/text()'.format(xpath_base))[
                    0].strip()
                depart = htmltree.xpath('{}[2]/text()'.format(xpath_base))[0]
                arrive = htmltree.xpath('{}[4]/text()'.format(xpath_base))[0]
                depart_time = datetime.strptime('{}-{}'.format(
                    search_date, depart.lower()), '%Y_%m_%d-%I:%M %p')
                arrive_time = datetime.strptime('{}-{}'.format(
                    search_date, arrive.lower()), '%Y_%m_%d-%I:%M %p')
                if arrive_time < depart_time:
                    arrive_time = arrive_time + timedelta(days=1)
                time_in_flight = arrive_time - depart_time
                h_in_flight = time_in_flight.seconds // 3600
                m_in_flight = (time_in_flight.seconds // 60) % 60
                flight_type = {}
                for k in range(5, 7):
                    try:
                        flight_class = htmltree.xpath(
                            '//*[@id="trip_{}_date_{}"]/thead/tr[2]/th[{}]/span/text()'.format(
                                rtrp + 1, search_date, k))[0]
                        cost = \
                            htmltree.xpath(
                                '{}[{}]/label/span/text()'.format(xpath_base,
                                                                  k + 1))[0]
                        currency = htmltree.xpath(
                            '{}[{}]/label/span/b/text()'.format(
                                xpath_base, k + 1))[0]
                        flight_type[flight_class] = str(cost + " " + currency)
                    except IndexError:
                        pass
                for key in ['Standard (1 Bag)', 'Discount (No Bags)']:
                    if key in flight_type:
                        fl_cost, fl_currency = flight_type[key].split()
                        fl_cost = int(''.join(fl_cost.split(',')))
                        f = Flight(depart_time,
                                   arrive_time,
                                   departure_airport if rtrp == 0 else arrive_airport,
                                   arrive_airport if rtrp == 0 else departure_airport,
                                   '{}h {}m'.format(h_in_flight, m_in_flight),
                                   flight,
                                   key,
                                   fl_cost,
                                   fl_currency
                                   )
                        flights.append(f)
            except IndexError:
                try:
                    err = htmltree.xpath(
                        '//*[@id="content"]/div/div[2]/div/text()')
                    if err:
                        print(err)
                except Exception:
                    pass
                break
    return flights


if __name__ == "__main__":
    try:
        if 3 > len(sys.argv) > 5 or \
                sys.argv[1].upper() not in airports or \
                sys.argv[2].upper() not in airports:
            raise ValueError
        departure = sys.argv[1].upper()
        arrive = sys.argv[2].upper()
        depart_date = date.fromisoformat(sys.argv[3])
        try:
            back_date = date.fromisoformat(sys.argv[4])
        except IndexError:
            back_date = None
    except Exception:
        print('Params are not valid')
        departure = airport_input('Departure:')
        arrive = airport_input('Destination:')
        depart_date, back_date = input_dates()

    my_params = {
        'AM': '{:0>4}-{:0>2}'.format(depart_date.year, depart_date.month),
        'AD': '{:0>2}'.format(depart_date.day),
        'DC': departure, 'AC': arrive, 'TT': 'OW'}
    if back_date:
        my_params.update({
            'RM': '{:0>4}-{:0>2}'.format(back_date.year, back_date.month),
            'RD': '{:0>2}'.format(back_date.day),
            'TT': 'RT'
        })
    try:
        answer = get_document_from_site(my_params)
    except Exception as ex:
        print('Some problems with website...')
        print(sys.exc_info()[1])
        exit(-1)
    all_flights = get_info_from_doc(answer, depart_date, back_date, departure,
                                    arrive)
    print('The following flights were found:')
    if not back_date:
        all_flights.sort(key=lambda fl: fl.cost)
        for index, fl in enumerate(all_flights):
            print(f'{index + 1}) ', end='')
            print(fl)
    else:
        foward_flights = []
        back_flights = []
        for i in all_flights:
            if i.depart_airport == departure:
                foward_flights.append(i)
            else:
                back_flights.append(i)
        comb = list(product(foward_flights, back_flights))
        comb.sort(key=lambda x: x[0].cost + x[1].cost)
        for index, i in enumerate(comb):
            if i[0].arrive_datetime < i[1].depart_datetime:
                print(f'{index + 1})', end='')
                print(f'{i[0].depart_airport} - {i[0].arrirve_airport},'
                      f'{i[1].depart_airport} - {i[1].arrirve_airport}:\n'
                      f'-{i[0].depart_datetime} - {i[0].arrive_datetime} '
                      f'({i[0].time_in_flight}) {i[0].flight} '
                      f'{i[0].type_flight}\n'
                      f'-{i[1].depart_datetime} - {i[1].arrive_datetime} '
                      f'({i[1].time_in_flight}) {i[1].flight} '
                      f'{i[1].type_flight}\n'
                      f'Total price {i[0].cost + i[1].cost} {i[0].currency}'
                      )
