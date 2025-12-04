#!/usr/bin/env python3

from collections import defaultdict
import sys


ORTHOGONAL_NEIGHBORS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]


def find_zeros_as_sources(level_map):
    counts = defaultdict(set)
    for row_no, row_data in enumerate(level_map):
        for col_no, col_char in enumerate(row_data):
            if col_char != "0":
                # Can't start here anyway.
                continue
            counts[(col_no, row_no)].add((col_no, row_no))
    return counts


def find_next_sources(current_sources, level_map, next_level_str):
    sources = defaultdict(set)
    w, h = len(level_map[0]), len(level_map)
    for (col_no, row_no), cell_sources in current_sources.items():
        for dx, dy in ORTHOGONAL_NEIGHBORS:
            n_col_no, n_row_no = col_no + dx, row_no + dy
            if not (0 <= n_col_no < w and 0 <= n_row_no < h):
                # Can't continue a trail outside the map
                continue
            n_char = level_map[n_row_no][n_col_no]
            if n_char != next_level_str:
                # Wrong height
                continue
            # Works!
            sources[(n_col_no, n_row_no)].update(cell_sources)
    return sources


def run(filename):
    with open(filename, "r") as fp:
        level_map = fp.read().strip().split("\n")
    current_sources = find_zeros_as_sources(level_map)
    # print(f"0 -> {current_sources}")
    for next_level in range(1, 9 + 1):
        current_sources = find_next_sources(current_sources, level_map, str(next_level))
        # print(f"{next_level} -> {current_sources}")
    print(f"{sum(len(cell_sources) for cell_sources in current_sources.values())=}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
