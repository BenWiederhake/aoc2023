#!/usr/bin/env python3

import re
import sys

RE_MUL = re.compile(r"mul\((\d+),(\d+)\)")


def find_muls(data):
    for match in RE_MUL.finditer(data):
        yield [int(e) for e in match.groups()]


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    the_sum = sum(a * b for a, b in find_muls(data))
    print(the_sum)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
