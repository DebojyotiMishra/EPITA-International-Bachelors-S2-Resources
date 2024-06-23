import random
import sys
import time

def make_arr(n):
    return sorted([random.randint(0, 2 * n - 1) for _ in range(n)])

def sort(arr):
    for l in range(len(arr) - 1):
        for r in range(l + 1, len(arr)):
            if arr[l] > arr[r]:
                arr[l], arr[r] = arr[r], arr[l]

def main():
    n = int(sys.argv[1])
    arr = make_arr(n)
    start = time.time()
    sort(arr)
    print(time.time() - start)