if __name__ == '__main__':
    s = input()

    alnum=False
    upper=False
    digit=False
    lower=False
    upper=False

    for ch in s:
        if ch.isalnum():
            alnum=True
        if ch.isalpha():
            alpha=True
        if ch.isdigit():
            digit=True
        if ch.islower():
            lower=True
        if ch.isupper():
            upper=True



    print('True' if alnum else 'False')
    print('True' if alpha else 'False')
    print('True' if digit else 'False')
    print('True' if lower else 'False')
    print('True' if upper else 'False')

