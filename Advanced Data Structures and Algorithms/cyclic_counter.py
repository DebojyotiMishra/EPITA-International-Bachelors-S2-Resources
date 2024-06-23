# A counter has a natural value, 0 at start time. 
# It can only be incremented or decremented by 1 at a time.
# Decrementing a null Counter is of no consequence

# ========== Cyclic Counter ==========
# Some counters may have a maximum value, given at creation time.
# For such counters, incrementing beyond the maximum value sets the value to 0.
# Decrementing a Counter below 0 sets the value to the maximum value.

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
        return f"C<{self.value}>"
    
if __name__ == "__main__":
    c = Counter(5)
    print(c)
    
    for i in range(10):
        c.increment()
    print(c)
    
    for i in range(5):
        c.decrement()
    print(c)