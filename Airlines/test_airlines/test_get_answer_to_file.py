from airlines import *

k = int(input('Number of requests'))
for _ in range(k):
    departure = airport_input('Departure:')
    arrive = airport_input('Destination:')
    depart_date, back_date = input_dates()
    answer = get_document_from_site(departure, arrive, depart_date, back_date)
    if not back_date:
        bkd = 'None'
    else:
        bkd = back_date
    name = f'Answers//Answer {departure} {arrive} {depart_date} ' \
           f'{bkd}.html'
    with open(name, 'w') as file:
        file.write(answer.text)
