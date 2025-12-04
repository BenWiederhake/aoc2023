#!/usr/bin/env python3

from collections import Counter
import sys


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    lines = data.split("\n")
    counts_first = Counter()
    counts_second = Counter()
    for l in lines:
        parts = l.split(" ")
        counts_first[int(parts[0])] += 1
        counts_second[int(parts[-1])] += 1
    print(counts_first)
    print(counts_second)
    similarity = sum(k * v * counts_second[k] for k, v in counts_first.items())
    print(similarity)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
