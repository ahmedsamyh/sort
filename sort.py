import random
import sys
import time
from typing import Callable, Tuple
import logging, coloredlogs

logging.basicConfig(level=logging.INFO)
coloredlogs.install(level=logging.INFO)

logger = logging.getLogger("sort")

sys.setrecursionlimit(2**int(32/2))

from threading import Thread

def todo(label: str):
    logger.info(f"TODO: {label}")
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
    et = (time.time() - t1)
    logger.info(f"Quick {et: 16.2}s")

def time_selectionsort(arr: list[int]):
    t1 = time.time()
    selectionsort(arr)
    et = (time.time() - t1)
    logger.info(f"Selec {et: 16.2}s")

def time_bubblesort(arr: list[int]):
    t1 = time.time()
    bubblesort(arr)
    et = (time.time() - t1)
    logger.info(f"Bubbl {et: 16.2}s")

def time_everything(arr: list[int]):
    threads: list[Thread] = []
    threads.append(Thread(target=time_quicksort, args=[arr]))
    threads.append(Thread(target=time_bubblesort, args=[arr]))
    threads.append(Thread(target=time_selectionsort, args=[arr]))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

def usage(program: str):
    logger.info(f"Usage: {program} <subcommand> [Flags] [Algorithm][s]")

algorithms_time_func_map: dict[str, Callable[ [list[int]], None]] = {
        "quick":      time_quicksort,
        "bubble":     time_bubblesort,
        "selection":  time_selectionsort,
        "everything": time_everything
 }

def hhelp():
    logger.info(f"Subcommands: ")
    logger.info(f"    time [Algorithm][s]         - Measure the time it takes to sort an array of N elements using the specified Algorithm.")
    logger.info(f"    print <arr> [Algorithm][s]  - Sort and print the given array.")
    logger.info(f"    help                        - Prints this help message.")
    logger.info(f"")
    logger.info(f"    Algorithm                   - One or more of bubblesort, quicksort, selectionsort, everything; DEFAULT: everything.")
    logger.info(f"")
    logger.info(f"Flags: ")
    logger.info(f"    -n                          - Specifies the number of elements in the array; DEFAULT: {DEFAULT_N}.")

def error(msg: str):
    logger.error(msg)

def calculate_random_array() -> list[int]:
    global N
    if N <= 0:
        logger.warning(f"N '{N}' was invalid, changing to default value '{DEFAULT_N}'")
        N = DEFAULT_N
    return [random.randint(0, MAX_VALUE) for _ in range(N)]

def parse_flag(program: str) -> bool:
    if len(sys.argv) <= 0: return False

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
                hhelp()
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
            hhelp()
            exit(1)
    return False

def expect_flag_with_value(expected_flag: str, value_not_provided_msg: str) -> Tuple[str, bool]:
    # NOTE: Prefix flag with - if not present
    if not expected_flag.startswith('-'): expected_flag = "-" + expected_flag
    value, found = "", False
    if len(sys.argv) <= 0: return ("", False)

    if sys.argv[0].startswith('-') and sys.argv[0] == expected_flag:
        sys.argv.pop(0)
        if len(sys.argv) <= 0:
            error(f"{value_not_provided_msg}")
            return ("", False)
        value, found = sys.argv.pop(0), True

    return value, found

def parse_algorithms(program: str) -> list[str]:
    algorithms: list[str] = []

    while len(sys.argv) > 0:
        algo: str = sys.argv.pop(0).lower()
        sort_prefix_present: bool = algo.endswith("sort")
        algo.removeprefix("sort")
        if algo in algorithms_time_func_map:
            if not sort_prefix_present: algo += "sort"
            algorithms.append(algo)
        else:
            error(f"Invalid Agolrithm '{algo}'")
            usage(program)
            hhelp()
            exit(1)

    # NOTE: Do every algorithms when nothing is provided
    if len(algorithms) <= 0: algorithms.append("everythingsort")

    return algorithms

def time_subcommand(program: str):
    # TODO: Replace with expect_flag_with_value
    while parse_flag(program):
        pass

    algorithms: list[str] = parse_algorithms(program)

    arr: list[int] = calculate_random_array()

    logger.info(f"Sorting {N} elements")

    for a in algorithms:
        a = a.removesuffix("sort")
        algorithms_time_func_map[a](arr)

def print_quicksort(arr: list[int]):
    logger.info(f"Quick Sort: {quicksort(arr, 0)}")

def print_selectionsort(arr: list[int]):
    logger.info(f"Selection Sort: {selectionsort(arr)}")

def print_bubblesort(arr: list[int]):
    logger.info(f"Bubble Sort: {bubblesort(arr)}")

def print_everything(arr: list[int]):
    threads: list[Thread] = []
    threads.append(Thread(target=print_quicksort, args=[arr.copy()]))
    threads.append(Thread(target=print_bubblesort, args=[arr.copy()]))
    threads.append(Thread(target=print_selectionsort, args=[arr.copy()]))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

algorithms_print_func_map: dict[str, Callable[[list[int]], None]] = {
        "quick":      print_quicksort,
        "bubble":     print_bubblesort,
        "selection":  print_selectionsort,
        "everything": print_everything
}

def print_subcommand(program: str):
    if len(sys.argv) <= 0:
        error("Please provide the array to be sorted!")
        usage(program)
        hhelp()
        exit(1)

    arr: list[int] = []
    try:
        arr = list(map(int, sys.argv.pop(0).split(' ')))
    except ValueError:
        error("Please pass only numbers in the array!")
        exit(1)

    algorithms: list[str] = parse_algorithms(program)

    logger.info(f"Sorting {len(arr)} elements")

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
            hhelp()
            exit(0)
        case "time":
            time_subcommand(program)
        case "print":
            print_subcommand(program)
        case '':
            error(f"Please provide a subcommand")
            usage(program)
            hhelp()
            exit(1)
        case _:
            error(f"Invalid subcommand '{subcmd}'")
            usage(program)
            hhelp()
            exit(1)

if __name__ == '__main__':
    main()

