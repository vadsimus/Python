class Myrange():
    def __init__(self, start, end, step=1):
        self.counter = start
        self.end = end
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < self.end:
            x = self.counter
            self.counter += self.step
            return x
        else:
            raise StopIteration


for i in Myrange(1, 100, 14):
    print(i)
