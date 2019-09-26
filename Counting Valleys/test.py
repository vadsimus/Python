import Counting_Valleys as CV
n=8
s='UDDDUDUU'
result = CV.countingValleys(n, s)
if result==1:
    print('Test1 pass')
else:
    print('Test1 fail')
n=12
s="DDUUDDUDUUUD"
result = CV.countingValleys(n, s)
if result==2:
    print('Test1 pass')
else:
    print('Test1 fail')