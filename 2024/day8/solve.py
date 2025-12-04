#!/usr/bin/env python3

from collections import defaultdict
import sys

CHAR_SPACE = "."


def gather_locations(level_map):
    w, h = len(level_map[0]), len(level_map)
    # For all possible antinode locations:
    for anti_y in range(h):
        for anti_x in range(w):
            # For all possible "close antenna locations":
            for acl_y in range(h):
                for acl_x in range(w):
                    acl_type = level_map[acl_y][acl_x]
                    if acl_type == CHAR_SPACE:
                        # No antenna at the "close" location!
                        continue
                    if (anti_x, anti_y) == (acl_x, acl_y):
                        # Whoops! An antenna isn't supposed to interfere with itself.
                        continue
                    # The "far" antenna must be at a location that is acl plus the difference vector:
                    afa_x = acl_x * 2 - anti_x
                    afa_y = acl_y * 2 - anti_y
                    if not (0 <= afa_x < w and 0 <= afa_y < h):
                        # There's no antennas outside the map.
                        continue
                    afa_type = level_map[afa_y][afa_x]
                    if afa_type != acl_type:
                        # Can't interfere with a different frequency.
                        # (Or no antenna at that location.)
                        continue
                    # Interference of two antennae at the same frequency that affect this anti-node!
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
