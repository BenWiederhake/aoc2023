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
    # If the problem was single-dimensional, then it would be a simple matter of computing the modulo inverse of the remainder, or something like that.
    # However, we're given that we need to push buttons at most 100 times, so simply brute-force it:
    for a_times in range(100 + 1):
        rx = px - ax * a_times
        ry = py - ay * a_times
        if rx % bx != 0 or ry % by != 0:
            # The remainder couldn't be solved by pressing the B button alone, so give up on this a_times.
            continue
        b_times_x = rx // bx
        b_times_y = ry // by
        if b_times_x != b_times_y:
            # Although each coordinate individually is possible, we can't achieve both at the same time.
            # TODO: This feels like it could be solved by bisecting the potential values of "a_times".
            # However, since it's 100 at most anyways, the performance gains are questionable.
            continue
        # It's possible!
        return 3 * a_times + 1 * b_times_x
    # Oh! Seems like the problem is impossible afterall.
    return 0


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    problems = list(parse_problems(data.split("\n")))
    print(problems)
    min_costs = []
    for problem in problems:
        min_costs.append(compute_min_cost(*problem))
    print(f"{min_costs=}")
    print(f"{sum(min_costs)=}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
