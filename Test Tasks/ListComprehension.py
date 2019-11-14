def squares(lst):
    return [x**2 for x in lst]

def even_elements(lst):
    return[x for i,x in enumerate(lst) if i%2==0]

def squares_even_on_odd(lst):
    """positions start from 1 """
    return[x**2 for i,x in enumerate(lst) if (i+1)%2!=0 and x%2==0]


lst=[x for x in range(1, 11)]
print(squares(lst))
print(even_elements(lst))
lst = [2,2,3,2,5,4,6]
print(squares_even_on_odd(lst))