#!/usr/bin/env python3

from collections import defaultdict
import sys

CHAR_OBSTACLE = "#"
CHAR_SPACE = "."
CHAR_SELF_UP = "^"


def scrub_map(level_map):
    for row_id, row_data in enumerate(level_map):
        for col_id, cell in enumerate(row_data):
            if cell == CHAR_SELF_UP:
                row_data[col_id] = CHAR_SPACE
                return (col_id, row_id, 0, -1)  # (0, -1) == "up"


def next_config(prev_config, level_map):
    x, y, dx, dy = prev_config
    x2, y2 = x + dx, y + dy
    w, h = len(level_map[0]), len(level_map)
    if not (0 <= x2 < w and 0 <= y2 < h):
        # Left the map
        return None
    in_front_of_you = level_map[y2][x2]
    if in_front_of_you == CHAR_OBSTACLE:
        # Turn right, i.e. (0, -1) becomes (1, 0) and (1, 0) becomes (0, 1).
        return (x, y, -dy, dx)
    # Step:
    return (x2, y2, dx, dy)


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    level_map = [list(substr) for substr in data.split("\n")]
    config = scrub_map(level_map)  # modifies 'level_map' in-place
    seen_configs = {config}
    while True:
        config = next_config(config, level_map)
        if config is None:
            print("We have left the map")
            break
        if config in seen_configs:
            print("infinite loop")
            break
        seen_configs.add(config)
    # Note that we accounted for configurations (which includes orientation), and not just positions.
    positions = {(x, y) for (x, y, dx, dy) in seen_configs}
    print(f"{len(positions)} unique positions")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
