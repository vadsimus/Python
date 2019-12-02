from airlines import get_info_from_doc, print_all_flights
import os
import sys
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
            bkd = datetime.strptime(data[4].split('.')[0], FRMT)


        all_flights = get_info_from_doc(answer,data[1], data[2])


        format_dt = '%Y-%m-%d %H:%M'
        for flight in all_flights:
            fl = (f'{flight.departure_airport}-{flight.arrive_airport}:'
                  f'{flight.flight} '
                  f'{flight.depart_datetime.strftime(format_dt)} - '
                  f'{flight.arrive_datetime.strftime(format_dt)} '
                  f'({flight.time_in_flight}) {flight.type_flight} '
                  f'{flight.cost} {flight.currency}')
            print(name, flight.flight, flight.depart_datetime, end='...')
            expected = str(next(reference))
            print(f'OK\ngot:     {fl.strip()} \nexpected:{expected}' if fl.strip() == expected.strip()
        else f'Fail\ngot:     {fl.strip()} \nexpected:{expected}')
