#!/usr/bin/env python3

from collections import Counter
import re
import sys

RE_FIRST = re.compile("^[^\d]*(\d).*$")
RE_LAST = re.compile("^.*(\d)[^\d]*$")


def contribution(line):
    first = RE_FIRST.match(line).group(1)
    last = RE_LAST.match(line).group(1)
    return int(first + last)


def solve(lines):
    return sum(contribution(line) for line in lines)


def as_lines(data):
    lines = data.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read()
    lines = as_lines(data)
    solution = solve(lines)
    print(solution)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("real.txt")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
