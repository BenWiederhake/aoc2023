#!/usr/bin/env python3

import sys


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    lines = data.split("\n")
    first_list = [int(l.split(" ")[0]) for l in lines]
    second_list = [int(l.split(" ")[-1]) for l in lines]
    first_list.sort()
    second_list.sort()
    distance = sum(abs(a - b) for a, b in zip(first_list, second_list))
    print(distance)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
