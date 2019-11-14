from Airlines import print_flights
from datetime import datetime
import json


def decode_objects(o):
    if '__datetime__' in o:
        return datetime.strptime(o['__datetime__'], '%Y-%m-%dT%H:%M:%S')
    return o


if __name__ == '__main__':
    with open('flights.json', ) as file:
        for line in file:
            all_fl = json.loads(line, object_hook=decode_objects)
            print_flights(all_fl)
