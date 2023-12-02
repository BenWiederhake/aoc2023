#!/usr/bin/env python3

from collections import Counter
import re
import sys

RE_GAME_ID = re.compile("^Game (\d+): (.+)$")
RE_COL_INFO = re.compile("^(\d+) (red|green|blue)")


def is_possible(seen):
    # "Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes."
    return seen["red"] <= 12 and seen["green"] <= 13 and seen["blue"] <= 14


def contribution(line):
    game_id, game_play = RE_GAME_ID.match(line).groups()
    game_id = int(game_id)  # LAZY
    for session in game_play.split("; "):
        # e.g. session = "1 green, 2 blue, 3 red, 6 blue"
        # (Not sure whether something crazy like that might happen.)
        seen = Counter()
        for col_info in session.split(", "):
            col_amount, col_name = RE_COL_INFO.match(col_info).groups()
            seen[col_name] += int(col_amount)
        if not is_possible(seen):
            return 0
    return int(game_id)


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
