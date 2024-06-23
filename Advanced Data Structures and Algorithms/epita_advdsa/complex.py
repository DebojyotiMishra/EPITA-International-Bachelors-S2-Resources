class Complex:
    def __init__(self, re = 0, im = 0):
        self.re = re
        self.im = im

    def __add__(self, other):
        return Complex(self.re + other.re, self.im + other.im)

    def __sub__(self, other):
        return Complex(self.re - other.re, self.im - other.im)

    def __mul__(self, other):
        return Complex(
            self.re * other.re - self.im * other.im, self.re * other.im + self.im * other.re
        )
    
    def __str__(self):
        return f"{self.re} + {self.im}i"

c1 = Complex(1, 2)
c2 = Complex(2, 1)

print(c1 + c2)
print(c1 - c2)
print(c1 * c2)
print(c1)