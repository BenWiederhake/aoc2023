#!/usr/bin/env python3

from collections import Counter
import re
import sys


RE_ROBOT = re.compile(r"^p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)$")
NUM_STEPS = 100
#LEVEL_WIDTH, LEVEL_HEIGHT = 11, 7
LEVEL_WIDTH, LEVEL_HEIGHT = 101, 103


# Derived config; do not edit!
assert LEVEL_WIDTH % 2 == 1
DISCRIMINANT_X = LEVEL_WIDTH // 2
assert LEVEL_HEIGHT % 2 == 1
DISCRIMINANT_Y = LEVEL_HEIGHT // 2


def parse_problems(lines):
    for line in lines:
        yield [int(e) for e in RE_ROBOT.match(line).groups()]


def predict_future_quadrant(robot):
    px, py, vx, vy = robot
    x = (px + NUM_STEPS * vx) % LEVEL_WIDTH
    y = (py + NUM_STEPS * vy) % LEVEL_HEIGHT
    quadrant = 0
    # print(f"{x=} {y=}")
    if x == DISCRIMINANT_X:
        return -1
    elif x > DISCRIMINANT_X:
        quadrant += 1
    if y == DISCRIMINANT_Y:
        return -1
    elif y > DISCRIMINANT_Y:
        quadrant += 2
    # print(f" -> {quadrant=}")
    return quadrant


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    robots = list(parse_problems(data.split("\n")))
    quadrant_counts = Counter(predict_future_quadrant(robot) for robot in robots)
    print(quadrant_counts)
    # Maybe use functools.prod or something:
    print(quadrant_counts[0] * quadrant_counts[1] * quadrant_counts[2] * quadrant_counts[3])


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
