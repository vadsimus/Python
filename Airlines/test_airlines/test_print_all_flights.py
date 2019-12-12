"""test airlines.print_all_flights"""
from airlines import print_all_flights
from collections import namedtuple
import json
from datetime import datetime


def datetime_conv(dic):
    """serialize datetime to ISO format"""
    if 'datetime' in dic:
        return datetime.fromisoformat(dic['datetime'])
    if 'date' in dic:
        return datetime.fromisoformat(dic['date'])



Flight = namedtuple(
    'Flight', ['depart_datetime', 'arrive_datetime',
               'departure_airport', 'arrive_airport',
               'flight', 'type_flight', 'cost', 'currency'])
with open('flights.json') as file:
    for line in file:
        forward = []
        back = []
        data = json.loads(line, object_hook=datetime_conv)
        for i, fls in enumerate(data[1]):
            for f in fls:
                flight = Flight(*f)
                if i==0:
                    forward.append(flight)
                else:
                    back.append(flight)
        if data[0][1]:
            bkd = data[0][1].date()
        else:
            bkd = None
        print('-' * 50)
        print('File: ', data[0][0])
        print('-' * 50)
        print_all_flights(bkd, forward, back)
