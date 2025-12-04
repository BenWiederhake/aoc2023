#!/usr/bin/env python3

import math
import sys


def contribution(race):
    time, distance = race
    # Need "> 0", so solve for the case that we beat the record by at least 1 second:
    determinant = time * time - 4 * (distance + 1)
    if determinant < 0:
        print(f"WARNING: Determinant is zero {time=} {distance=}")
        return 0

    hold_min_raw = (time - math.sqrt(determinant)) / 2
    hold_min = math.ceil(hold_min_raw)
    assert (time - hold_min) * hold_min >= distance + 1, f"{time=} {distance=} {determinant=} {hold_min_raw=} {hold_min=}"
    if (time - (hold_min - 1)) * (hold_min - 1) >= distance + 1:
        # In this case, hold_min_raw should have been an integer, and ceil() erroneously "rounded up" to the next integer.
        # Note that technically, the error with floating point can be much larger than this, e.g. when trying to represent gigantic numbers.
        print(f"IT HAPPENED! {time=} {distance=} {hold_min_raw=} {hold_min=} -> MUST DECREMENT!")
        hold_min -= 1
    assert (time - hold_min) * hold_min >= distance + 1, f"{time=} {distance=} {hold_min=}"
    hold_max = time - hold_min
    if hold_max < hold_min:
        print(f"WARNING: Rounding eliminated options {time=} {distance=} {hold_min=} {hold_max=}")
        return 0
    return hold_max - hold_min + 1


def solve(races):
    return math.prod(contribution(race) for race in races)


def as_races(data):
    lines = data.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    assert len(lines) == 2
    times = lines[0].split()
    distances = lines[1].split()
    assert len(times) == len(distances), (len(times), len(distances))
    assert times[0] == "Time:"
    assert distances[0] == "Distance:"
    races = []
    for time, distance in zip(times[1 :], distances[1 :]):
        races.append((int(time), int(distance)))
    return races


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read()
    races = as_races(data)
    solution = solve(races)
    print(solution)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("real.txt")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
