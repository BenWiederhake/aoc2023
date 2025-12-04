#!/usr/bin/env python3

from math import gcd
import re
import sys


RE_EXPECTED = [
    re.compile(r"^Button A: X\+(\d+), Y\+(\d+)$"),
    re.compile(r"^Button B: X\+(\d+), Y\+(\d+)$"),
    re.compile(r"^Prize: X=(\d+), Y=(\d+)$"),
    re.compile(r"^$"),
]
MAGIC_OFFSET = 10000000000000


def parse_problems(lines):
    lines.append("")
    assert len(lines) % 4 == 0
    num_problems = len(lines) // 4
    for i in range(num_problems):
        # ".groups" would crash if there's no match, i.e. a syntax error.
        matches = [line_re.match(lines[i * 4 + line_in_problem]).groups() for line_in_problem, line_re in enumerate(RE_EXPECTED)]
        matches = matches[: -1]
        yield matches


def intify(tuple_of_strings):
    return [int(e) for e in tuple_of_strings]


def compute_min_cost(a_xy, b_xy, prize_xy):
    ax, ay = intify(a_xy)
    bx, by = intify(b_xy)
    px, py = intify(prize_xy)
    px += MAGIC_OFFSET
    py += MAGIC_OFFSET
    del a_xy, b_xy, prize_xy
    # Simplify x coordinates:
    gcd_x = gcd(ax, bx)
    ax //= gcd_x
    bx //= gcd_x
    if px % gcd_x != 0:
        return 0
    px //= gcd_x
    del gcd_x
    # Simplify y coordinates:
    gcd_y = gcd(ay, by)
    ay //= gcd_y
    by //= gcd_y
    if py % gcd_y != 0:
        return 0
    py //= gcd_y
    del gcd_y
    # At this point, a and b are co-prime on each axis.
    # Assume we know a_times, and we want to know b_times, then we have:
    #   px = ax * a_times + bx * b_times
    #   py = ay * a_times + by * b_times
    #   -> b_times = (px - ax * a_times) / bx
    #   -> b_times = (py - ay * a_times) / by
    # Note that we have two equations for b_times! This means we can equate them:
    #   (px - ax * a_times) / bx = (py - ay * a_times) / by
    # Oh look! We can now drop the assumption that we know a_times, and in fact calculate it directly:
    #   (px - ax * a_times) * by = (py - ay * a_times) * bx
    #   -> px * by - ax * a_times * by = py * bx - ay * a_times * bx
    #   -> a_times * (-ax * by + ay * bx) = py * bx - px * by
    #   -> a_times = (py * bx - px * by) / (ay * bx - ax * by)
    # This feels like there is some deeper geometrical understanding I should be able to gleam from this.
    a_times_numerator = py * bx - px * by
    a_times_denominator = ay * bx - ax * by
    assert a_times_denominator != 0, f"a/b vectors are co-linear! This would need some interesting case-distinctions, but apparently this doesn't actually appear in the input."
    if a_times_numerator % a_times_denominator != 0:
        return 0
    a_times = a_times_numerator // a_times_denominator
    del a_times_numerator, a_times_denominator
    if (px - ax * a_times) % bx != 0:
        # TODO: What's the intuition for this case?
        return 0
    b_times = (px - ax * a_times) // bx
    return 3 * a_times + 1 * b_times


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    problems = list(parse_problems(data.split("\n")))
    min_costs = []
    for problem in problems:
        min_costs.append(compute_min_cost(*problem))
    # print(f"{min_costs=}")
    print(f"{sum(min_costs)=}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
