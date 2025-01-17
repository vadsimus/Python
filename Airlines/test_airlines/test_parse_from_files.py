from airlines import get_info_from_doc
import os
from datetime import datetime

FRMT = '%Y-%m-%d'
path = './/Answers'


def ref_data():
    file = open('flights.txt', 'r')
    for line in file:
        yield line
    file.close()


for root, dirs, files in os.walk(path, topdown=False):
    reference = ref_data()
    for name in files:
        file_path = os.path.join(root, name)
        with open(file_path, 'r') as file:
            answer = file.read()
        data = name.split()
        if data[4].split('.')[0] == 'None':
            bkd = None
        else:
            bkd = datetime.strptime(data[4].split('.')[0], FRMT).date()
        all_flights = get_info_from_doc(
            answer, data[1], data[2],
            datetime.strptime(data[3].split('.')[0], FRMT).date(), bkd)
        format_dt = '%Y-%m-%d %H:%M'
        for flights in all_flights:
            for flight in flights:
                time_in_flight = flight.arrive_datetime - flight.depart_datetime
                h_in_flight = time_in_flight.seconds // 3600
                m_in_flight = (time_in_flight.seconds // 60) % 60
                time_in_flight = '{}h {}m'.format(h_in_flight, m_in_flight)
                fl = (f'{flight.departure_airport}-{flight.arrive_airport}:'
                      f'{flight.flight} '
                      f'{flight.depart_datetime.strftime(format_dt)} - '
                      f'{flight.arrive_datetime.strftime(format_dt)} '
                      f'({time_in_flight}) {flight.type_flight} '
                      f'{int(flight.cost) if flight.cost.is_integer() else flight.cost} '
                      f'{flight.currency}')
                print(name, flight.flight, flight.depart_datetime, end='...')
                expected = str(next(reference))
                print(
                    f'OK\ngot:     {fl.strip()} \nexpected:{expected}'
                    if fl.strip() == expected.strip()
                    else f'Fail\ngot:     {fl.strip()} \nexpected:{expected}')
