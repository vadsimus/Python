from Airlines import *
from datetime import datetime

if __name__ == '__main__':
    with open('Answer.html') as file:
        answer = file.read()
    doc = lxml.html.document_fromstring(answer)
    depart_date = datetime.strptime('15-11-19', '%d-%m-%y')
    back_date = datetime.strptime('16-11-19', '%d-%m-%y')
    forward_flights = get_info_from_doc(doc, depart_date, False)
    back_flights = get_info_from_doc(doc, back_date, True)


    def test_flight(flight, ref: dict, prompt):
        print('{:.<10}'.format(prompt), end='')
        for key in ref.keys():
            if key not in flight.keys() or flight[key] != ref[key]:
                print("Fail")
                return
        print("Ok")


    test_flight(forward_flights[0], {'depart_date': '2019_11_15',
                                     'depart_time': datetime(2019, 11, 15, 10, 30),
                                     'arrive_time': datetime(2019, 11, 15, 12, 40),
                                     'Standard (1 Bag)': ' 13,907 PKR'},
                'Forward1')
    test_flight(forward_flights[1], {'depart_date': '2019_11_15',
                                     'depart_time': datetime(2019, 11, 15, 21, 0),
                                     'arrive_time': datetime(2019, 11, 15, 23, 10),
                                     'Standard (1 Bag)': ' 13,907 PKR'},
                'Forward2')
    test_flight(back_flights[0], {'depart_date': '2019_11_16',
                                  'depart_time': datetime(2019, 11, 16, 7, 30),
                                  'arrive_time': datetime(2019, 11, 16, 9, 40),
                                  'Standard (1 Bag)': ' 13,907 PKR'},
                'Back1')
    test_flight(back_flights[1], {'depart_date': '2019_11_16',
                                  'depart_time': datetime(2019, 11, 16, 18, 0),
                                  'arrive_time': datetime(2019, 11, 16, 20, 10),
                                  'Standard (1 Bag)': ' 13,907 PKR'},
                'Back1')
