from Airlines.airlines import get_document_from_site
from datetime import datetime, date

departure = 'JED'
arrive = 'ISB'
depart_date = datetime(2019, 12, 5)
back_date = datetime(2019, 12, 7)
my_params = {
    'AM': '{:0>4}-{:0>2}'.format(depart_date.year, depart_date.month),
    'AD': '{:0>2}'.format(depart_date.day),
    'DC': departure, 'AC': arrive, 'TT': 'OW'}
if back_date:
    my_params.update({
        'RM': '{:0>4}-{:0>2}'.format(back_date.year, back_date.month),
        'RD': '{:0>2}'.format(back_date.day),
        'TT': 'RT'})

answer = get_document_from_site(my_params)
with open(f'Answers//Answer {departure} {arrive} {depart_date.date()} '
          f'{back_date.date()}.html', 'w') as file:
    file.write(answer.text)
