"""test airlines.print_all_flights"""
from collections import namedtuple
import json
from datetime import datetime
from airlines import print_all_flights


def datetime_conv(dic):
    """serialize datetime to ISO format"""
    if 'datetime' in dic:
        return datetime.fromisoformat(dic['datetime'])
    return repr(dic)


Flight = namedtuple(
    'Flight', ['depart_datetime', 'arrive_datetime',
               'departure_airport', 'arrive_airport',
               'time_in_flight', 'flight',
               'type_flight', 'cost', 'currency'])
with open('flights.json') as file:
    for line in file:
        data = json.loads(line, object_hook=datetime_conv)
        all_flights = []
        for f in data[1]:
            flight = Flight(*f)
            all_flights.append(flight)
        print('-' * 50)
        print('File: ', data[0][2])
        print('-' * 50)
        print_all_flights(all_flights, data[0][0], data[0][1])
