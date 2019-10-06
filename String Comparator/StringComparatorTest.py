
import StringComparator as SC
from functools import cmp_to_key


print ('Test1 start')
n = 4
inp=[['davis',20],['davis',15],['edgehill',15],['davis',10]]
data = []
for i in range(n):
    name, score = inp[i][0],inp[i][1]
    score = int(score)
    player = SC.Player(name, score)
    data.append(player)
    
data = sorted(data, key=cmp_to_key(SC.Player.comparator))
for i in data:
    print(i.name, i.score)