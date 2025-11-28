#!/usr/bin/env python3

from collections import Counter
import re
import sys

# Something special happens after:
# - 50 s (horizontal? line)
# - 95 s (vertical line)
# - 153 s (horizontal line)
# - 196 s (vertical line)
# That's a period of 103 and 101 each. Huh. What a coincidence.
# After 101*103 seconds, everything is back to the start, because (px + vx*101*103) = px mod 101, similarly for y.
# Guess: Make those "special" occurrences line up.
# Horizontal happens at 50 mod 103.
# Vertical happens at 95 mod 101.
# The only number with these properties is …
# How do you solve diophantine equations again?
# So we're looking for n = 50 + k * 103 such that 50 + k * 2 = 95 (mod 101), i.e. 2k = 45 (mod 101), i.e. k = 73.
# Therefore n = 7569 is a solution, plus arbitrary multiples of 101*103.
# Testing …
# Success! :D


# LEVEL_WIDTH, LEVEL_HEIGHT = 11, 7
LEVEL_WIDTH, LEVEL_HEIGHT = 101, 103

RE_ROBOT = re.compile(r"^p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)$")
SYMBOLS = {
    # (is_upper, is_lower)
    (False, False): "_",
    (False, True): "▄",
    (True, False): "▀",
    (True, True): "█",
}


def parse_problems(lines):
    for line in lines:
        yield [int(e) for e in RE_ROBOT.match(line).groups()]


def display(num_steps, robots):
    presences = set()
    for robot in robots:
        px, py, vx, vy = robot
        x = (px + num_steps * vx) % LEVEL_WIDTH
        y = (py + num_steps * vy) % LEVEL_HEIGHT
        presences.add((x, y))
    print()
    print(f"==========[ After {num_steps} seconds ]==========")
    for y_half in range((LEVEL_HEIGHT + 1) // 2):
        for x in range(LEVEL_WIDTH):
            y_up = y_half * 2
            y_lo = y_half * 2 + 1
            up_present = (x, y_up) in presences
            lo_present = (x, y_lo) in presences
            symbol_to_render = SYMBOLS[(up_present, lo_present)]
            print(symbol_to_render, end="")
        print()


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    robots = list(parse_problems(data.split("\n")))
    # i = 0
    i = 7569 - 5
    while True:
        display(i, robots)
        input("Continue? (Press Enter or Ctrl-C)")
        i += 1


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
