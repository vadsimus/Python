def generator():
    while True:
        yield 'Hello'

g = generator()
for _ in range(5):
    print(next(g))