#!/usr/bin/env python3

from collections import defaultdict
import sys

ALLOWED_CORNERS = {
    "MSMS",
    "MSSM",
    "SMMS",
    "SMSM",
}


def parse_grid(data):
    return data.split("\n")  # lol


def get_from_grid(grid, x, y):
    if 0 <= y < len(grid):
        line = grid[y]
        if 0 <= x < len(line):
            return line[x]
    return '.'


def xmas_at(grid, x, y):
    if "A" != get_from_grid(grid, x, y):
        return 0
    corners = ''.join(get_from_grid(grid, x + dx, y + dy) for dx, dy in [(1, 1), (-1, -1), (1, -1), (-1, 1)])
    return corners in ALLOWED_CORNERS


def count_xmases(grid):
    width = len(grid[0])
    height = len(grid)
    xmases = 0
    for y in range(height):
        for x in range(width):
            xmases += xmas_at(grid, x, y)
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
