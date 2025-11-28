#!/usr/bin/env python3

from collections import defaultdict
import sys


CACHE = dict()
MAX_CACHE = 2023


def determine_length(number, depth):
    global CACHE
    cached = CACHE.get((number, depth), None)
    if cached is None:
        cached = determine_length_slowcase(number, depth)
        if number <= MAX_CACHE:
            CACHE[(number, depth)] = cached
    return cached


def determine_length_slowcase(number, depth):
    if depth == 0:
        return 1
    assert depth > 0
    if number == 0:
        return determine_length(1, depth - 1)
    n_str = str(number)
    if len(n_str) % 2 == 0:
        # Even length! Break the sequence of digits apart as a string:
        midpoint = len(n_str) // 2
        lhs = int(n_str[: midpoint])
        rhs = int(n_str[midpoint :])
        del n_str  # be nice to gc
        return determine_length(lhs, depth - 1) + determine_length(rhs, depth - 1)
    else:
        del n_str  # be nice to gc
        return determine_length(number * 2024, depth - 1)


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    numbers = [int(part) for part in data.split(" ")]
    lengths = [determine_length(n, 75) for n in numbers]
    print(f"{len(CACHE)=}")
    print(f"{sum(lengths)=}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
