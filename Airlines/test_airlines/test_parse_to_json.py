"""Create json file by all answers"""
import os
import json
from datetime import datetime
from airlines import get_info_from_doc

FRMT = '%Y-%m-%d'
PATH = './/Answers'


def datetime_convert(datet):
    """Convet datetime format to dict"""
    if isinstance(datet, datetime):
        return {'datetime': datet.isoformat()}
    return repr(datet)


for root, dirs, files in os.walk(PATH, topdown=False):
    for name in files:
        file_path = os.path.join(root, name)
        with open(file_path, 'r') as file:
            answer = file.read()
        data = name.split()
        if data[4].split('.')[0] == 'None':
            bkd = None
        else:
            bkd = datetime.strptime(data[4].split('.')[0], FRMT)
        all_flights = get_info_from_doc(answer, data[1], data[2])
        flight_info = [data[1], bkd, name]
        all_flights_and_info = [flight_info, all_flights]
        with open('flights.json', 'a') as file:
            json.dump(all_flights_and_info, file, default=datetime_convert)
            file.write('\n')
