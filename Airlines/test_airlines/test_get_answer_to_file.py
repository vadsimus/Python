
from airlines import get_document_from_site
from datetime import datetime, date

departure = 'AUH'
arrive = 'KHI'
depart_date = datetime(2019, 12, 2)
# back_date = datetime(2019, 12, 2)
back_date = ''

answer = get_document_from_site(departure, arrive, depart_date, back_date)
if not back_date:
    bkd = 'None'
else:
    bkd = back_date.date
with open(f'Answers//Answer {departure} {arrive} {depart_date.date()} '
          f'{bkd}.html', 'w') as file:
    file.write(answer.text)
