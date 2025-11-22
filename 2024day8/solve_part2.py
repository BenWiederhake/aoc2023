#!/usr/bin/env python3

from collections import defaultdict
from math import gcd
import sys

CHAR_SPACE = "."


def gather_locations(level_map):
    w, h = len(level_map[0]), len(level_map)
    max_distance = max(w, h)
    # For all possible "antenna1" locations:
    for a1_y in range(h):
        for a1_x in range(w):
            a1_type = level_map[a1_y][a1_x]
            if a1_type == CHAR_SPACE:
                # No antenna at the "1" location!
                continue
            # For all possible "antenna2" locations:
            for a2_y in range(h):
                for a2_x in range(w):
                    a2_type = level_map[a2_y][a2_x]
                    if a2_type != a1_type:
                        # Can't interfere with a different frequency.
                        # (Or no antenna at that location.)
                        continue
                    if (a1_x, a1_y) == (a2_x, a2_y):
                        # Whoops! An antenna isn't supposed to interfere with itself.
                        continue
                    # These two antennae interfere, hooray!
                    # We need to walk the entire infinite line between thes antennae.
                    dx, dy = a2_x - a1_x, a2_y - a1_y
                    # But if the distance is not simplified (e.g. (7, 0) or (2, 4)), simplify it first:
                    d_gcd = gcd(dx, dy)
                    dx, dy = dx // d_gcd, dy // d_gcd
                    del d_gcd
                    # Now, walk the line in both directions:
                    for k in range(-max_distance, max_distance + 1):
                        anti_x = a1_x + dx * k
                        anti_y = a1_y + dy * k
                        if not (0 <= anti_x < w and 0 <= anti_y < h):
                            # There's no antinodes outside the map.
                            continue
                        # Found an anti-node!
                        yield (anti_x, anti_y)


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    level_map = data.split("\n")
    locations = list(gather_locations(level_map))
    print(f"{len(set(locations))=}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
