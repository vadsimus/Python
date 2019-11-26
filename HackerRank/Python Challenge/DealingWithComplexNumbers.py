# https://www.hackerrank.com/challenges/class-1-dealing-with-complex-numbers/problem


class Complex(object):
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary

    def __add__(self, no):
        return (Complex(self.real + no.real, self.imaginary + no.imaginary))

    def __sub__(self, no):
        return (Complex(self.real - no.real, self.imaginary - no.imaginary))

    def __mul__(self, no):
        a1 = self.real
        b1 = self.imaginary
        a2 = no.real
        b2 = no.imaginary
        rl = (a1 * a2) - (b1 * b2)
        im = (a1 * b2) + (b1 * a2)
        return (Complex(rl, im))

    def __truediv__(self, no):
        a1 = self.real
        b1 = self.imaginary
        a2 = no.real
        b2 = no.imaginary
        rl = ((a1 * a2) + (b1 * b2)) / ((a2 ** 2) + (b2 ** 2))
        im = ((a2 * b1) - (a1 * b2)) / ((a2 ** 2) + (b2 ** 2))
        return (Complex(rl, im))

    def mod(self):
        return Complex(((self.real ** 2) + (self.imaginary ** 2)) ** 0.5, 0)

    def __str__(self):
        if self.imaginary == 0:
            result = "%.2f+0.00i" % (self.real)
        elif self.real == 0:
            if self.imaginary >= 0:
                result = "0.00+%.2fi" % (self.imaginary)
            else:
                result = "0.00-%.2fi" % (abs(self.imaginary))
        elif self.imaginary > 0:
            result = "%.2f+%.2fi" % (self.real, self.imaginary)
        else:
            result = "%.2f-%.2fi" % (self.real, abs(self.imaginary))
        return result


if __name__ == '__main__':
    c = map(float, input().split())
    d = map(float, input().split())
    x = Complex(*c)
    y = Complex(*d)
    print(*map(str, [x + y, x - y, x * y, x / y, x.mod(), y.mod()]), sep='\n')
