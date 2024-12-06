#!/usr/bin/env python3

from collections import defaultdict
import sys


def parse_grid(data):
    return data.split("\n")  # lol


def get_from_grid(grid, x, y):
    if 0 <= y < len(grid):
        line = grid[y]
        if 0 <= x < len(line):
            return line[x]
    return '.'


def xmas_at(grid, x0, y0, dx, dy):
    maybe_xmas = ''.join(get_from_grid(grid, x0 + dx * i, y0 + dy * i) for i in range(4))
    return maybe_xmas == "XMAS"


def count_xmases(grid):
    width = len(grid[0])
    height = len(grid)
    xmases = 0
    for y0 in range(height):
        for x0 in range(width):
            xmases += xmas_at(grid, x0, y0, +1, 0)
            xmases += xmas_at(grid, x0, y0, +1, +1)
            xmases += xmas_at(grid, x0, y0, 0, +1)
            xmases += xmas_at(grid, x0, y0, -1, +1)
            xmases += xmas_at(grid, x0, y0, -1, 0)
            xmases += xmas_at(grid, x0, y0, -1, -1)
            xmases += xmas_at(grid, x0, y0, 0, -1)
            xmases += xmas_at(grid, x0, y0, +1, -1)
    return xmases


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    grid = parse_grid(data.strip())
    xmases = count_xmases(grid)
    print(xmases)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
