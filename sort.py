import random
import sys
import time

sys.setrecursionlimit(2**int(32/2))

from threading import Thread

def quicksort(arr, depth) -> []:
    if len(arr) == 1:
        return [arr[0]]

    # Take the first element as the pivot
    pivot = arr.pop(0)

    left = []
    right = []
    for i in arr:
        if i <= pivot:
            left.append(i)
        else:
            right.append(i)

    nl = []
    nr = []
    if len(left):
        nl = quicksort(left, depth+1)
    if len(right):
        nr = quicksort(right, depth+1)

    nl.append(pivot)
    for i in nr:
        nl.append(i)

    return nl

def bubblesort(arr) -> []:
    for _ in range(len(arr)):
        for i in range(len(arr)-1):
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]

    return arr

def bubblesort_better(arr) -> []:
    arr_sorted = False
    while not arr_sorted:
        arr_sorted = True
        for i in range(len(arr)-1):
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                arr_sorted = False

def bubblesort_best(arr) -> []:
    arr_sorted = False
    sorted_count = 0
    while not arr_sorted:
        arr_sorted = True
        for i in range(len(arr)-1-sorted_count):
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                arr_sorted = False
        sorted_count += 1

def time_quicksort(arr):
    t1 = time.time()
    quicksort(arr.copy(), 0)
    print(f"Quick Sort took %.2fs" % (time.time() - t1))

# def time_bubblesort(arr):
#     t1 = time.time()
#     bubblesort(arr.copy())
#     print(f"Bubble Sort took %.2fs" % (time.time() - t1))

# def time_bubblesort_better(arr):
#     t1 = time.time()
#     bubblesort_better(arr.copy())
#     print(f"Bubble Sort Better took %.2fs" % (time.time() - t1))

# def time_bubblesort_best(arr):
#     t1 = time.time()
#     bubblesort_best(arr.copy())
#     print(f"Bubble Sort Best took %.2fs" % (time.time() - t1))

def time_bubblesort(arr):
    t1 = time.time()
    bubblesort_best(arr.copy())
    print(f"Bubble Sort Best took %.2fs" % (time.time() - t1))




def usage(program: str):
    print(f"Usage: {program} [SORT_ALGORITHM | N] [N]")

def hhelp(program: str):
          print(f"\tSORT_ALGORITHM can be [\"bubblesort\", \"quicksort\"]; By default does every algorithm")
          print(f"\tN is the number of elements in the list to be sorted; Default is 1000")

def error(msg: str):
    print(f"ERROR: {msg}", file=sys.stderr)
    exit(1)

def main():

    program: str = sys.argv.pop(0)

    N: int = 1000

    cmd: str = ""
    try:
        cmd = sys.argv.pop(0)
        if cmd.isdigit():
            N = int(cmd)
            if N <= 0:
                error("N cannot be <= 0 dummy")
            cmd = ""
    except Exception:
        pass

    match cmd:
        case "help":
            usage(program)
            hhelp(program)
            exit(0)

    try:
        N = int(sys.argv.pop(0))
        if N <= 0:
            error("N cannot be <= 0 dummy")
    except Exception:
        pass
    MAX = 2**3
    arr = [random.randint(0, MAX) for _ in range(N)]

    print(f"Sorting {N} elements:")

    threads = []
    match cmd.lower():
        case "":
            threads.append(Thread(target=time_bubblesort, args=[arr]))
            threads.append(Thread(target=time_quicksort, args=[arr]))
        case "bubble" | "bubblesort":
            threads.append(Thread(target=time_bubblesort, args=[arr]))
        case "quick" | "quicksort":
            threads.append(Thread(target=time_quicksort, args=[arr]))
        case _:
            print(f"ERROR: Invalid command '{cmd}'")
            exit(1)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()

