import random
import sys
import time

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


_timing_from: float = 0.0
_timing_label: str = ''

def time_from(label: str):
    global _timing_from, _timing_label

    _timing_label = label
    _timing_from = time.time()

def time_here():
    global _timing_from

    elapsed_timing = time.time() - _timing_from

    print(f"PROFILE: [{_timing_label}] took %.2fs" % elapsed_timing)


def time_quicksort(arr):
    t1 = time.time()
    quicksort(arr.copy(), 0)
    print(f"Quick Sort took %.2fs" % (time.time() - t1))

def time_bubblesort(arr):
    t1 = time.time()
    bubblesort(arr.copy())
    print(f"Bubble Sort took %.2fs" % (time.time() - t1))

def time_bubblesort_better(arr):
    t1 = time.time()
    bubblesort_better(arr.copy())
    print(f"Bubble Sort Better took %.2fs" % (time.time() - t1))

def time_bubblesort_best(arr):
    t1 = time.time()
    bubblesort_best(arr.copy())
    print(f"Bubble Sort Best took %.2fs" % (time.time() - t1))


def main():
    N = 1000
    try:
        N = int(sys.argv[1])
    except:
        pass

    MAX = 2**32
    arr = [random.randint(0, MAX) for _ in range(N)]

    print(f"Sorting {N} elements:")
    threads = []

    threads.append(Thread(target=time_quicksort, args=[arr]))
    threads.append(Thread(target=time_bubblesort, args=[arr]))
    threads.append(Thread(target=time_bubblesort_better, args=[arr]))
    threads.append(Thread(target=time_bubblesort_best, args=[arr]))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()

