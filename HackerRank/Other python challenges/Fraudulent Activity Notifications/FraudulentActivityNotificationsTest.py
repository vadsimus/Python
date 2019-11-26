import FraudulentActivityNotifications as Fan
import FANTooLong


def testFAN(exps: str, d: int, expect: int, number=1, tl=False):
    """tl=True to use FANTooLong func
    """
    print('Test{}{} ...'.format(number, "TL" if tl else ''), end='')
    exp = list(map(int, exps.rstrip().split()))
    result = FANTooLong.activityNotificationsTooLong(exp, d) if tl else Fan.activityNotifications(exp, d)
    print('your:{}...expected:{}...'.format(result, expect), end='')
    print('OK' if result == expect else "Fail")


if __name__ == "__main__":
    testFAN('2 3 4 2 3 6 8 4 5', 5, 2, 1)
    testFAN('10 20 30 40 50', 3, 1, 2)
    testFAN('1 2 3 4 4', 4, 0, 3)
    testFAN('8 2 7 3 9 6 1 9', 4, 1, 4)
    testFAN('5 2 1 0 9 7 2 9 0 8', 4, 3, 5)
    testFAN('0 1 2 3 4 5 4 8 0 2 3 9 0 8 0 2 9', 6, 4, 6)
    testFAN('2 2 2 2 4 8', 4, 2, 7)

    with open('test8.txt', 'r') as file:
        testFAN(file.read(), 10000, 633, 8)

    testFAN('0 0 0 2 2 2 8', 4, 3, 9)
    testFAN('1 1 1 5 5 5 9 8 8 8 8 8', 6, 1, 10)

    testFAN('2 3 4 2 3 6 8 4 5', 5, 2, 1, True)
    testFAN('10 20 30 40 50', 3, 1, 2, True)
    testFAN('1 2 3 4 4', 4, 0, 3, True)
    testFAN('8 2 7 3 9 6 1 9', 4, 1, 4, True)
    testFAN('5 2 1 0 9 7 2 9 0 8', 4, 3, 5, True)
    testFAN('0 1 2 3 4 5 4 8 0 2 3 9 0 8 0 2 9', 6, 4, 6, True)
    testFAN('2 2 2 2 4 8', 4, 2, 7, True)
    testFAN('1 1 1 5 5 5 9 8 8 8 8 8', 6, 1, 10, True)
