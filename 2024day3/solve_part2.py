#!/usr/bin/env python3

import re
import sys

RE_INSN = re.compile(r"mul\((\d+),(\d+)\)|do\(\)|don't\(\)")


def compute(data):
    acc = 0
    enabled = True
    for match in RE_INSN.finditer(data):
        if match.group(0) == "do()":
            enabled = True
        elif match.group(0) == "don't()":
            enabled = False
        elif enabled:
            a, b = match.groups()
            acc += int(a) * int(b)
    return acc


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    print(compute(data))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
