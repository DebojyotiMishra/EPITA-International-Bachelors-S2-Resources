# A counter has a natural value, 0 at start time. 
# It can only be incremented or decremented by 1 at a time.
# Decrementing a null Counter is of no consequence


class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def decrement(self):
        if self.value > 0:
            self.value -= 1

    def __str__(self):
        return f"C<{self.value}>"


if __name__ == "__main__":
    c = Counter()
    print(c)

    # Incrementing the counter 10 times
    for i in range(10):
        c.increment()
    print(c)

    # Decrementing the counter 20 times
    for i in range(20):
        c.decrement()
    print(c)
