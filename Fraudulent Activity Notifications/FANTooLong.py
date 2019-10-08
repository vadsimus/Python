#This function work right, but too long. Was used to create data for tests


def activityNotificationsTooLong(expenditure, d):
    def median(a):
        a.sort()
        l=int(len(a)/2)
        if len(a)%2==0:
            return (a[l]+a[(l-1)])/2
        return a[l]
    exp = expenditure
    counter = 0
    for i in range(d,len(exp)):
        if exp[i]>=2*median(exp[i-d:i].copy()):
            counter+=1
    return counter