#!/usr/bin/env python3

from collections import Counter
import re
import sys

LOOKUP = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}
REGEX_OPTIONS = "|".join(LOOKUP.keys())

RE_FIRST = re.compile(f"^(?:(?!{REGEX_OPTIONS}).)*({REGEX_OPTIONS}).*$")
RE_LAST = re.compile(f"^.*({REGEX_OPTIONS})(?:(?!{REGEX_OPTIONS}).)*$")
print(f"{RE_FIRST=}")
print(f"{RE_LAST=}")


def contribution(line):
    print(f">>{line}<<")
    print(f"  -> {RE_FIRST.match(line).groups()=}")
    print(f"  -> {RE_LAST.match(line).groups()=}")
    try:
        first = RE_FIRST.match(line).group(1)
        last = RE_LAST.match(line).group(1)
        first_digit = LOOKUP[first]
        last_digit = LOOKUP[last]
        return first_digit * 10 + last_digit
    except BaseException as e:
        print(f"On input line >>{line}<<")
        raise e


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
