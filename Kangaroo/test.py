import Kangaroo as K
result = K.kangaroo(0, 3, 4, 2)
if result=="YES":
    print("Test1 Pass")
else:
    print('Test1 fail')
result = K.kangaroo(0, 2, 5, 3)
if result=="NO":
    print("Test2 Pass")
else:
    print('Test2 fail')
