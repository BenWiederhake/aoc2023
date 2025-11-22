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


def gets_stuck_in_loop(initial_config, level_map):
    seen_configs = {initial_config}
    config = initial_config
    while True:
        config = next_config(config, level_map)
        if config is None:
            return False
        if config in seen_configs:
            return True
        seen_configs.add(config)


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    level_map = [list(substr) for substr in data.split("\n")]
    initial_config = scrub_map(level_map)  # modifies 'level_map' in-place
    options = 0
    for row_id in range(len(level_map)):
        print(f"Now testing row {row_id} of {len(level_map)} …")
        for col_id in range(len(level_map[0])):
            if initial_config[0] == col_id and initial_config[1] == row_id:
                # Can't put anything there!
                continue
            if level_map[row_id][col_id] == CHAR_OBSTACLE:
                # Can't put anything there either!
                continue
            # Let's try it out!
            level_map[row_id][col_id] = CHAR_OBSTACLE
            option_is_viable = gets_stuck_in_loop(initial_config, level_map)
            level_map[row_id][col_id] = CHAR_SPACE
            if option_is_viable:
                options += 1
    print(f"{options} options!")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
