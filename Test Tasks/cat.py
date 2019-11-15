import sys
for a in sys.argv[1:]:
    try:
        with open(a, 'r')as file:
            s = file.read()
            print(s)
    except IOError:
        print("Can't read file")