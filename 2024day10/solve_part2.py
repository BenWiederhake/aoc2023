#!/usr/bin/env python3

from collections import defaultdict
import sys


ORTHOGONAL_NEIGHBORS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]


def find_zeros_as_counts(level_map):
    counts = defaultdict(int)
    for row_no, row_data in enumerate(level_map):
        for col_no, col_char in enumerate(row_data):
            if col_char != "0":
                # Can't start here anyway.
                continue
            counts[(col_no, row_no)] += 1
    return counts


def find_next_counts(current_counts, level_map, next_level_str):
    counts = defaultdict(int)
    w, h = len(level_map[0]), len(level_map)
    for (col_no, row_no), cell_count in current_counts.items():
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
            counts[(n_col_no, n_row_no)] += cell_count
    return counts


def run(filename):
    with open(filename, "r") as fp:
        level_map = fp.read().strip().split("\n")
    # Fun fact! Due to a misunderstanding, this is what I implemented *first*, and now have to write again, lol.
    current_counts = find_zeros_as_counts(level_map)
    for next_level in range(1, 9 + 1):
        current_counts = find_next_counts(current_counts, level_map, str(next_level))
    print(f"{sum(current_counts.values())=}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
