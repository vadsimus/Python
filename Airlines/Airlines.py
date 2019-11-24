from urllib import request, parse
import sys
from datetime import datetime, date, time
airports = {'AUH': 'Abu Dhabi', 'DXB': 'Dubai', 'DMM': 'Dammam',
            'ISB': 'Islmabad', 'JED': 'Jeddah', 'KHI': 'Karachi',
            'LHE': 'Lahore', 'MED': 'Medina', 'MUX': 'Multan',
            'MCT': 'Muscat', 'PEW': 'Peshawar', 'RYK': 'Rahim Yar Khan',
            'UET': 'Quetta', 'RUH': 'Riyadh', 'SHJ': 'Sharjah',
            'SKT': 'Sialkot'}

class Flight:
    def __init__(self, depart_date, depart_airport, target_aiport, back_date = None):
        self.depart_date = depart_date
        self.depart_airport = depart_airport
        self.target_airport = target_aiport
        self.back_date = back_date


def input_date(direction):
    if direction == "Forward":
        prompt = 'Date of flight out {YYYY-MM-DD}:'
    elif direction == "Back":
        prompt = 'Date to return back {YYYY-MM-DD} or empty:'
    while True:
        inp = input(prompt)
        if inp == '' and direction == 'Back':
            return None
        elif inp == '' and direction == 'Forward':
            print("Depart date can't be empty!")
            continue
        try:
            dt = date.fromisoformat(inp)
        except ValueError:
            print('Wrong format, try once else..')
            continue
        if dt < date.today():
            print(f"Date can't be in past. Today is {date.today().isoformat()}")
            continue
        else:
            return dt


def airport_input(prompt):
    print('Input airport (AUH,DXB,...) or help')
    while True:
        airport = input(prompt).upper().strip()
        if airport in airports:
            print(airports[airport])
            return airport
        if airport == 'HELP':
            for ap in airports:
                print(ap, ':', airports[ap])
                continue
        print("Airport input is invalid.")


if __name__ == "__main__":
    try:
        if 3 < len(sys.argv) > 6 or sys.argv[1].upper() not in airports or sys.argv[2].upper() not in airports:
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
        depart_date = input_date('Forward')
        back_date = input_date('Back')

    print(f'departure={departure} arrive={arrive} depart_date={depart_date} back_date={back_date}')
