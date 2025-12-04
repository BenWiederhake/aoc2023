#!/usr/bin/env python3

from collections import defaultdict
import sys

CHAR_OBSTACLE = "#"
CHAR_SPACE = "."
CHAR_SELF_UP = "^"


def goal_if_solvable(eqn):
    goal_str, parts_str = eqn.split(": ")
    goal = int(goal_str)
    del goal_str
    parts = [int(p) for p in parts_str.split(" ")]
    del parts_str
    possible_values = {parts[0]}
    # print(f"{goal=}, {parts=}, {possible_values=}")
    for part in parts[1:]:
        next_possible_values = set()
        next_possible_values.update(pv + part for pv in possible_values)
        next_possible_values.update(pv * part for pv in possible_values)
        next_possible_values.update(int(f"{pv}{part}") for pv in possible_values)
        possible_values = next_possible_values
        # possible_values = {pv for pv in next_possible_values if pv <= goal}
        del next_possible_values
        # print(f"  -> {possible_values=}")
    print(f"set has size {len(possible_values)}")
    if goal in possible_values:
        return goal
    return None


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    sum_solvable = 0
    for eqn in data.split("\n"):
        reached_goal = goal_if_solvable(eqn)
        if reached_goal is not None:
            sum_solvable += reached_goal
    print(f"{sum_solvable=}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
