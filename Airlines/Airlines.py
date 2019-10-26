from urllib import request, parse
import sys
import re
import lxml.html
from datetime import datetime


def create_date(string):
    try:
        dt = datetime.strptime(string, '%d-%m-%y')
        return dt
    except ValueError or TypeError:
        return None


def input_date(direction):
    if direction == "Forward":
        prompt = 'Date of flight out {DD MM YY} or today:'
    elif direction == "Back":
        prompt = 'Date to return back {DD MM YY} or empty:'
    today = datetime.now()
    while True:
        date = list(re.split('[ \-_]', input(prompt)))
        if date[0] == 'today':
            return today
        elif date[0].strip() == '' and direction == 'Back':
            return None
        elif date[0].strip() == '' and direction == 'Forward':
            print("Depart date can't be empty!")
            continue
        elif create_date('-'.join(date)):
            d = create_date('-'.join(date))
            if d < today:
                print("Date can't be in past. Today is {}-{}-{}".format(
                    today.day, today.month, today.year))
                continue
            return d
        else:
            print('Wrong!!!')


def airport_input(prompt):
    airports = {'AUH': 'Abu Dhabi', 'DXB': 'Dubai', 'DMM': 'Dammam',
                'ISB': 'Islmabad', 'JED': 'Jeddah', 'KHI': 'Karachi',
                'LHE': 'Lahore', 'MED': 'Medina', 'MUX': 'Multan',
                'MCT': 'Muscat', 'PEW': 'Peshawar', 'RYK': 'Rahim Yar Khan',
                'UET': 'Quetta', 'RUH': 'Riyadh', 'SHJ': 'Sharjah',
                'SKT': 'Sialkot'}
    print('Input airport (AUH,DXB,...) or help')
    while True:
        airport = input(prompt)
        for ap in airports:
            if airport.upper().strip() == ap:
                print(airports[ap])
                return ap
        if airport.lower() == 'help':
            for ap in airports:
                print(ap, ':', airports[ap])
                continue
        print("Airport input is invalid.")


def get_document_from_site(my_params):
    myUrl = "https://www.airblue.com/bookings/flight_selection.aspx?"
    value = {'TT': 'RT', 'RD': my_params['RD'], 'FL': 'on', 'CC': 'Y', 'CD': '',
             'PA': '1', 'PC': '', 'PI': '', 'x': '40', 'y': '20',
             'AD': my_params['AD'], 'AM': my_params['AM'],
             'RM': my_params['RM'], 'DC': my_params['DC'],
             'AC': my_params['AC']}
    mydata = parse.urlencode(value)
    myUrl = myUrl + mydata
    req = request.Request(myUrl)
    answer = request.urlopen(req)
    answer = answer.read().decode('UTF-8')
    document = lxml.html.document_fromstring(answer)
    return document


def get_info_from_doc(doc, depart_date, roundtrip):
    flights = []
    if roundtrip:
        rtrp = '2'
    else:
        rtrp = '1'
    flights_counter = 1
    while True:
        flight_info = {}
        try:
            xpath_base = '//*[@id="trip_{}_date_{}"]/tbody[{}]/tr/td'
            xpath_base = xpath_base.format(rtrp, depart_date, flights_counter)
            flight = doc.xpath('{}[1]/text()'.format(xpath_base))[0].strip()
            depart = doc.xpath('{}[2]/text()'.format(xpath_base))[0]
            arrive = doc.xpath('{}[4]/text()'.format(xpath_base))[0]
            k = 5
            flight_type = {}
            while True:
                try:
                    flight_class = doc.xpath(
                        '//*[@id="trip_{}_date_{}"]/thead/tr[2]/th[{}]/span/text()'.format(
                            rtrp, depart_date, k))[0]
                    coast = \
                        doc.xpath('{}[{}]/label/span/text()'.format(xpath_base,
                                                                    k + 1))[0]
                    currency = doc.xpath(
                        '{}[{}]/label/span/b/text()'.format(
                            xpath_base, k + 1))[0]
                    flight_type[flight_class] = str(coast + " " + currency)
                    k += 1
                except IndexError:
                    break
            flight_info["depart_date"] = (depart_date)
            flight_info['flight'] = (flight)
            depart_time = datetime.strptime(depart.lower(), '%I:%M %p')
            flight_info['depart_time'] = (
                datetime.strftime(depart_time, '%H:%M'))
            arrive_time = datetime.strptime(arrive.lower(), '%I:%M %p')
            flight_info['arrive_time'] = (
                datetime.strftime(arrive_time, '%H:%M'))
            time_in_flight = arrive_time - depart_time
            h_in_flight = time_in_flight.seconds // 3600
            m_in_flight = (time_in_flight.seconds // 60) % 60
            flight_info['time_in_flight'] = '{}h {}m'.format(
                h_in_flight, m_in_flight)
            for ft in flight_type:
                flight_info[ft] = (flight_type[ft])
            flights_counter += 1
            flights.append(flight_info)
        except IndexError:
            try:
                err = doc.xpath('//*[@id="content"]/div/div[2]/div/text()')
                if err:
                    print(err)
            except Exception:
                break
            break
    return flights


def print_flights(mass_flights):
    max_len = 0
    sep = str('-' * 20) + '+'
    exclusive_keys = []
    forward_flights = mass_flights[0]
    if len(mass_flights) == 2:
        back_flights = mass_flights[1]
    else:
        back_flights = []
    for k in mass_flights:
        for i in k:
            if len(i) >= max_len:
                max_len = len(i)
    header = ['Direction', 'Date', 'Flight', 'Depart Time', 'Arrive Time',
              'Time in air']
    sequence = ["depart_date", 'flight', 'depart_time', 'arrive_time',
                'time_in_flight']
    for i in forward_flights:
        for key in i:
            if key not in sequence and key not in exclusive_keys:
                exclusive_keys.append(key)
    for flight in back_flights:
        for key in flight:
            if key not in sequence and key not in exclusive_keys:
                exclusive_keys.append(key)
    for i in header:
        print("{:^20}".format(i), end='|')
    for i in exclusive_keys:
        print("{:^20}".format(i), end='|')
    print()
    print(sep * (len(header) + len(exclusive_keys)))
    for fl in forward_flights:
        print("{:^20}".format('Forward'), end='|')
        for key in fl:
            if key in sequence:
                print("{:^20}".format(fl[key]), end='|')
        for ex_key in exclusive_keys:
            if ex_key in fl.keys():
                print("{:^20}".format(fl[ex_key]), end='|')
            else:
                print(' ' * 20, end='|')
        print()
    if len(mass_flights) == 2:
        print(sep * (len(header) + len(exclusive_keys)))
        for flight in back_flights:
            print("{:^20}".format('Back'), end='|')
            for key in flight:
                if key in sequence:
                    print("{:^20}".format(flight[key]), end='|')
            for ex_key in exclusive_keys:
                if ex_key in flight.keys():
                    print("{:^20}".format(flight[ex_key]), end='|')
                else:
                    print(' ' * 20, end='|')
            print()


if __name__ == '__main__':
    departure = airport_input('Departure:')
    arrive = airport_input('Destination:')
    depart_date = input_date('Forward')
    back_date = input_date('Back')
    back_date_flag = True
    if back_date is None or back_date < depart_date:
        if back_date:
            print("Back date can't be before depart date.")
        back_date_flag = False
        back_date = depart_date
    my_params = {'AM': '{}-{}'.format(depart_date.year, depart_date.month),
                 'AD': '{}'.format(depart_date.day),
                 'RM': '{}-{}'.format(back_date.year, back_date.month),
                 'RD': '{}'.format(back_date.day),
                 'DC': departure,
                 'AC': arrive}
    try:
        doc = get_document_from_site(my_params)
    except Exception:
        print('Some problems with site...')
        print(sys.exc_info()[1])
        exit(-1)
    forward_flights = get_info_from_doc(doc, '{}_{}_{}'.format(
        depart_date.year, depart_date.month, depart_date.day), False)
    all_flights = [forward_flights]
    if back_date_flag:
        back_flights = get_info_from_doc(doc, '{}_{}_{}'.format(
            back_date.year, back_date.month, back_date.day), True)
        all_flights.append(back_flights)
    print_flights(all_flights)
