#!/usr/bin/env python3

import math
import sys


class ResolvableValue:
    def __init__(self, initial_value):
        self.current = initial_value
        self.last = None

    def consider_mapping(self, dst_start, src_start, length):
        if self.last is not None:
            # Already mapped
            return
        offset = self.current - src_start
        if 0 <= offset < length:
            self.last = self.current
            self.current = dst_start + offset

    def commit(self):
        self.last = None


def solve(lines):
    assert len(lines) > 10, lines
    seed_parts = lines[0].split()
    assert seed_parts[0] == "seeds:"
    seeds = [ResolvableValue(int(seed_part)) for seed_part in seed_parts[1 :]]
    assert lines[1] == ""

    for i, line in enumerate(lines[2 :]):
        if line.endswith(" map:"):
            continue
        if not line:
            for seed in seeds:
                seed.commit()
            continue
        parts = line.split()
        assert len(parts) == 3, (i + 2, line)
        dst_start = int(parts[0])
        src_start = int(parts[1])
        length = int(parts[2])
        for seed in seeds:
            seed.consider_mapping(dst_start, src_start, length)
    return min(seed.current for seed in seeds)


def as_lines(data):
    lines = data.split("\n")
    # No cleanup necessary! Trailing emptyline doesn't matter.
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
