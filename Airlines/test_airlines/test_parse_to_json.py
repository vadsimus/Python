import os
from airlines import *
import json

FRMT = '%Y-%m-%d'
path = './/Answers'


def datetime_convert(o):
    if isinstance(o, datetime):
        return {'datetime': o.isoformat()}
    if isinstance(o, date):
        return {'date': o.isoformat()}


for root, dirs, files in os.walk(path, topdown=False):
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
        all_flights_and_info = [[name, bkd], all_flights]
        with open('flights.json', 'a') as file:
            json.dump(all_flights_and_info, file, default=datetime_convert)
            file.write('\n')
