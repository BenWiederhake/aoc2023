#!/usr/bin/env python3

from collections import Counter
import re
import sys

RE_GAME_ID = re.compile("^Game (\d+): (.+)$")
RE_COL_INFO = re.compile("^(\d+) (red|green|blue)")


def contribution(line):
    # Want to compute the minimum set needed, and then the power.
    minimum_needed = Counter()

    game_id, game_play = RE_GAME_ID.match(line).groups()
    game_id = int(game_id)  # LAZY
    for session in game_play.split("; "):
        # e.g. session = "1 green, 2 blue, 3 red, 6 blue"
        # (Not sure whether something crazy like that might happen.)
        seen = Counter()
        for col_info in session.split(", "):
            col_amount, col_name = RE_COL_INFO.match(col_info).groups()
            seen[col_name] += int(col_amount)
        for col_name, col_amount in seen.items():
            minimum_needed[col_name] = max(minimum_needed[col_name], col_amount)

    # Now compute the power:
    akku = 1
    # Ill-defined for missing colors. Should we multiply by 0 then?
    minimum_needed["red"]
    minimum_needed["green"]
    minimum_needed["blue"]
    for col_amount in minimum_needed.values():
        akku *= col_amount
    return akku


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
