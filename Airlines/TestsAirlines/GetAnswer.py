from Airlines import *
import lxml

departure = airport_input('Departure:')
arrive = airport_input('Destination:')
depart_date = input_date('Forward')
back_date = input_date('Back')
if back_date is None or back_date < depart_date:
    if back_date:
        print(
            "Back date can't be before forward depart date. One way trip is shown.")
    back_flag = False
else:
    back_flag = True
my_params = {
    'AM': '{:0>4}-{:0>2}'.format(depart_date.year, depart_date.month),
    'AD': '{:0>2}'.format(depart_date.day),
    'DC': departure, 'AC': arrive}
if back_flag:
    my_params['RM'] = '{:0>4}-{:0>2}'.format(back_date.year,
                                             back_date.month)
    my_params['RD'] = '{:0>2}'.format(back_date.day)
try:
    doc = get_document_from_site(my_params, back_flag)
except Exception as ex:
    print('Some problems with website...')
    print(sys.exc_info()[1])
    exit(-1)
answer = lxml.html.tostring(doc, encoding='UTF-8')
with open('Answer.html', 'wb') as file:
    file.write(answer)

if back_flag:
    forward_flights = get_info_from_doc(doc, depart_date, False)
    all_flights = [forward_flights]
    back_flights = get_info_from_doc(doc, back_date, True)
    all_flights.append(back_flights)
else:
    forward_flights = get_info_from_doc(doc, depart_date, False)
    all_flights = [forward_flights]

print_flights(all_flights)
