import sys
import random
import time


def make_arr(n):
    return sorted([random.randint(0, 2 * n - 1) for _ in range(n)])


def sequential_search(arr, x):
    start_time = time.monotonic_ns()
    for i in range(len(arr)):
        if arr[i] == x:
            end_time = time.monotonic_ns()
            return i, end_time - start_time
    end_time = time.monotonic_ns()
    return -1, end_time - start_time


def binary_search(arr, x):
    start_time = time.monotonic_ns()
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == x:
            end_time = time.monotonic_ns()
            return mid, end_time - start_time
        elif arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    end_time = time.monotonic_ns()
    return -1, end_time - start_time


if __name__ == "__main__":
    n = int(sys.argv[1])
    target = int(sys.argv[2])
    arr = make_arr(n)
    
    # method = sys.argv[3]
    # if method == "-s":
    #     index, time_taken = sequential_search(arr, target)
    #     print(f"Sequential Search: Target is at index: {index}, Time taken: {time_taken} nano-seconds")
    # elif method == "-b":
    #     index, time_taken = binary_search(arr, target)
    #     print(f"Binary Search: Target is at index: {index}, Time taken: {time_taken} nano-seconds")
    # else:
    #     print("Invalid method. Please use -s for sequential search or -b for binary search.")
        
    print("\n\n")
    print("================== DOING SEARCHES ==================")

    index, time_taken = sequential_search(arr, target)
    print(f"Sequential Search: Target is at index: {index}, Time taken: {time_taken} nano-seconds")

    index, time_taken = binary_search(arr, target)
    print(f"Binary Search: Target is at index: {index}, Time taken: {time_taken} nano-seconds")
    
    print("================== END OF SEARCHES ==================")
    print("\n\n")