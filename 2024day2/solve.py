#!/usr/bin/env python3

import sys


def gen_reports(data):
    for line in data.split("\n"):
        yield [int(number) for number in line.split(" ")]


def is_increasing(report):
    for i in range(len(report) - 1):
        diff = report[i + 1] - report[i]
        if not (1 <= diff <= 3):
            return False
    return True


def is_decreasing(report):
    for i in range(len(report) - 1):
        diff = report[i + 1] - report[i]
        if not (-3 <= diff <= -1):
            return False
    return True


def is_safe(report):
    return is_increasing(report) or is_decreasing(report)


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    num_safe = sum(is_safe(report) for report in gen_reports(data))
    print(num_safe)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
