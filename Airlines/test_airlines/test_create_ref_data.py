import os
from datetime import datetime
from Airlines.airlines import *

FRMT = '%Y-%m-%d'
path = './/Answers'

for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        file_path = os.path.join(root, name)
        with open(file_path, 'r') as file:
            answer = file.read()
        data = name.split()
        all_flights = get_info_from_doc(answer,
                                        datetime.strptime(data[3], FRMT),
                                        datetime.strptime(
                                            data[4].split('.')[0], FRMT),
                                        data[1], data[2])

        for f in all_flights:
            file = open('flights.txt', 'a')
            sys.stdout = file
            print_flight(f)
            file.close()
