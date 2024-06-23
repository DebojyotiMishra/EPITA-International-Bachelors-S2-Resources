class Counter:
    def __init__(self, max_value):
        self.value = 0
        self.max_value = max_value

    def increment(self):
        if self.value == self.max_value:
            self.value = 0
        else:
            self.value += 1

    def decrement(self):
        if self.value == 0:
            self.value = self.max_value
        else:
            self.value -= 1

    def __str__(self):
        return f"{self.value}"


class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.h = Counter(23)
        self.m = Counter(59)
        self.s = Counter(59)

    def increment(self):
        if self.s.value == 59:
            self.m.increment()
            if self.m.value == 59:
                self.h.increment()
                if self.h.value == 23:
                    self.h.value = 0
        self.s.increment()

    def decrement(self):
        if self.s.value == 0:
            self.m.decrement()
            if self.m.value == 0:
                self.h.decrement()
                if self.h.value == 0:
                    self.h.value = 23
        self.s.decrement()

    def __str__(self):
        return f"{self.h.value}:{self.m.value}:{self.s.value}"


if __name__ == "__main__":
    s = Stopwatch()

    for i in range(1000):
        s.increment()
    print(f"{s}")

    for i in range(2000):
        s.decrement()
    print(f"{s}")
