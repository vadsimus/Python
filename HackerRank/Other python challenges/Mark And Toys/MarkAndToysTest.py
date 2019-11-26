import MarkAndToys as MT

k=7
pr=[1, 2, 3, 4]
r=MT.maximumToys(pr, k)
print('test1:','OK' if r==3 else "Fail")

k=50
pr=[1, 12, 5, 111, 200, 1000, 10]
r=MT.maximumToys(pr, k)
print('test2:','OK' if r==4 else "Fail")


