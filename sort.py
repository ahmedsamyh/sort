import random
import sys
import time
from typing import Callable

sys.setrecursionlimit(2**int(32/2))

from threading import Thread

def todo(label: str):
    print(f"TODO: {label}")
    exit(1)

DEFAULT_N: int = 1000
N: int = DEFAULT_N
MAX_VALUE: int = 2**32

def quicksort(arr, depth) -> list[int]:
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

def bubblesort(arr) -> list[int]:
    result = arr.copy()
    arr_sorted = False
    sorted_count = 0
    while not arr_sorted:
        arr_sorted = True
        for i in range(len(arr)-1-sorted_count):
            if result[i] > result[i+1]:
                result[i], result[i+1] = result[i+1], result[i]
                arr_sorted = False
        sorted_count += 1
    return result

def selectionsort(arr) -> list[int]:
    result = arr.copy()
    for i in range(len(arr)-1):
        for j in range(i+1, len(arr)):
            if result[i] > result[j]:
                result[i], result[j] = result[j], result[i]
        # print(f"Sorted: {result[0:i]} | \tUnsorted: {result[i:len(result)]}")
    return result

def time_quicksort(arr: list[int]):
    t1 = time.time()
    quicksort(arr, 0)
    print(f"Quick Sort took %.2fs" % (time.time() - t1))

def time_selectionsort(arr: list[int]):
    t1 = time.time()
    selectionsort(arr)
    print(f"Selection Sort took %.2fs" % (time.time() - t1))

def time_bubblesort(arr: list[int]):
    t1 = time.time()
    bubblesort(arr)
    print(f"Bubble Sort Best took %.2fs" % (time.time() - t1))

def time_everything(arr: list[int]):
    threads: list[Thread] = []
    threads.append(Thread(target=time_bubblesort, args=[arr]))
    threads.append(Thread(target=time_bubblesort, args=[arr]))
    threads.append(Thread(target=time_selectionsort, args=[arr]))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

def usage(program: str):
    print(f"Usage: {program} <subcommand> [Flags] [Algorithm][s]")

algorithms_time_func_map: dict[str, Callable[ [list[int]], None]] = {
        "quick":      time_quicksort,
        "bubble":     time_bubblesort,
        "selection":  time_selectionsort,
        "everything": time_everything
 }

def hhelp(program: str):
    print((f"Subcommands: \n"
           f"    time [Algorithm][s]         - Measure the time it takes to sort an array of N elements using the specified Algorithm.\n"
           f"    sort <arr> [Algorithm][s]   - Sort a given"
           f"    help                        - Prints this help message.\n"
           f"\n"
           f"    Algorithm                   - One or more of bubblesort, quicksort, selectionsort, everything; DEFAULT: everything.\n"
           f"\n"
           f"Flags: \n"
           f"    -n                          - Specifies the number of elements in the array; DEFAULT: {DEFAULT_N}."))

def error(msg: str):
    print(f"ERROR: {msg}", file=sys.stderr)

def calculate_random_array() -> list[int]:
    global N
    if N <= 0:
        print(f"WARNING: N '{N}' was invalid, changing to default value '{DEFAULT_N}'")
        N = DEFAULT_N
    return [random.randint(0, MAX_VALUE) for _ in range(N)]

def parse_flag(program: str) -> bool:
    if len(sys.argv) <= 0: return ""

    flag: str = ""
    if sys.argv[0].startswith('-'):
        flag = sys.argv.pop(0)

    flag = flag.removeprefix('-')
    match flag:
        case 'n':
            global N
            def invalid_n_func() -> None:
                error("Please provide a number after -n!")
                usage(program)
                hhelp(program)
                exit(1)

            if len(sys.argv) <= 0:
                invalid_n_func()
            try:
                N = int(sys.argv.pop(0))
            except ValueError:
                invalid_n_func()
            return True
        case '':
            pass
        case _:
            error(f"Invalid flag '{flag}'")
            usage(program)
            hhelp(program)
            exit(1)
    return False

def expect_flag_with_value(program: str, expected_flag: str, value_not_provided_msg: str) -> (str, bool):
    # NOTE: Prefix flag with - if not present
    if not expected_flag.startswith('-'): expected_flag = "-" + expected_flag
    value, found = "", False
    if len(sys.argv) <= 0: return ("", False)

    if sys.argv[0].startswith('-') and sys.argv[0] == expected_flag:
        flag: str = sys.argv.pop(0)
        if len(sys.argv) <= 0:
            error(f"{value_not_provided_msg}")
            return ("", False)
        value, found = sys.argv.pop(0), True

    return value, found

def parse_algorithms(program: str) -> list[str]:
    algorithms: list[str] = []

    while len(sys.argv) > 0:
        algo: string = sys.argv.pop(0).lower()
        sort_prefix_present: bool = algo.endswith("sort")
        algo.removeprefix("sort")
        if algo in algorithms_time_func_map:
            if not sort_prefix_present: algo += "sort"
            algorithms.append(algo)
        else:
            error(f"Invalid Aglorithm '{algo}'")
            usage(program)
            hhelp(program)
            exit(1)

    # NOTE: Do every algorithms when nothing is provided
    if len(algorithms) <= 0: algorithms.append("everythingsort")

    return algorithms

def time_subcommand(program: str):
    algorithms: list[str] = parse_algorithms(program)

    # TODO: Replace with expect_flag_with_value
    while parse_flag(program):
        pass

    arr: list[int] = calculate_random_array()

    print(f"Sorting {N} elements")

    for a in algorithms:
        a = a.removesuffix("sort")
        algorithms_time_func_map[a](arr)

def print_quicksort(arr: list[int]):
    print(f"Quick Sort: {quicksort(arr, 0)}")

def print_selectionsort(arr: list[int]):
    print(f"Selection Sort: {selectionsort(arr)}")

def print_bubblesort(arr: list[int]):
    print(f"Bubble Sort: {bubblesort(arr)}")

def print_everything(arr: list[int]):
    threads: list[Thread] = []
    threads.append(Thread(target=print_bubblesort, args=[arr]))
    threads.append(Thread(target=print_bubblesort, args=[arr]))
    threads.append(Thread(target=print_selectionsort, args=[arr]))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

algorithms_print_func_map: dict[str, Callable[[], None]] = {
        "quick":      print_quicksort,
        "bubble":     print_bubblesort,
        "selection":  print_selectionsort,
        "everything": print_everything
}

def print_subcommand(program: str):
    if len(sys.argv) <= 0:
        error("Please provide the array to be sorted!")
        usage(program)
        hhelp(program)
        exit(1)

    arr: list[int] = []
    try:
        arr = list(map(int, sys.argv.pop(0).split(' ')))
    except ValueError:
        error("Please pass only numbers in the array!")
        exit(1)

    algorithms: list[str] = parse_algorithms(program)

    print(f"Sorting {len(arr)} elements")

    for a in algorithms:
        a = a.removesuffix("sort")
        algorithms_print_func_map[a](arr)

def main():
    program: str = sys.argv.pop(0)

    # Parse subcommand
    subcmd: str = ""
    if len(sys.argv) > 0: subcmd = sys.argv.pop(0)

    match subcmd.lower():
        case "help":
            usage(program)
            hhelp(program)
            exit(0)
        case "time":
            time_subcommand(program)
        case "print":
            print_subcommand(program)
        case '':
            error(f"Please provide a subcommand")
            usage(program)
            hhelp(program)
            exit(1)
        case _:
            error(f"Invalid subcommand '{subcmd}'")
            usage(program)
            hhelp(program)
            exit(1)

if __name__ == '__main__':
    main()

