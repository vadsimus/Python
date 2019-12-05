import os
from airlines import *

FRMT = '%Y-%m-%d'
path = './/Answers'
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

        for f in all_flights:
            file = open('flights.txt', 'a')
            sys.stdout = file
            print_flight(f)
            file.close()
