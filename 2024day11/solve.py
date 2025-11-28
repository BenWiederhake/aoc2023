#!/usr/bin/env python3

from collections import defaultdict
import sys


def generate_new_numbers(numbers):
    # print("Begin generation")
    for n in numbers:
        # print(f"  consider {n}")
        if n == 0:
            yield 1
            continue
        n_str = str(n)
        if len(n_str) % 2 == 0:
            # Even length! Break the sequence of digits apart as a string:
            midpoint = len(n_str) // 2
            yield int(n_str[: midpoint])
            yield int(n_str[midpoint: ])
        else:
            yield n * 2024


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    numbers = [int(part) for part in data.split(" ")]
    for _ in range(25):
        numbers = list(generate_new_numbers(numbers))
    print(f"{len(numbers)=}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
