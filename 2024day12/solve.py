#!/usr/bin/env python3

from collections import defaultdict
import sys


def generate_neighbors(x, y):
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = x + dx, y + dy
        yield (nx, ny)


def discover_region(level_map, x, y):
    w, h = len(level_map[0]), len(level_map)
    plant = level_map[y][x]
    if not isinstance(plant, str):
        # Replacement object from an earlier run!
        return 0, 0
    marker = object()
    level_map[y][x] = marker
    todo_stack = [(x, y)]
    area = 1
    perimeter = 0
    while todo_stack:
        x, y = todo_stack.pop()
        for nx, ny in generate_neighbors(x, y):
            if not (0 <= nx < w and 0 <= ny < h):
                # Outside
                perimeter += 1
                continue
            n_type = level_map[ny][nx]
            if n_type is marker:
                # no perimeter, no extension:
                pass
            elif n_type == plant:
                # no perimeter, but do extend:
                level_map[ny][nx] = marker
                area += 1
                todo_stack.append((nx, ny))
            else:
                # Different plant (doesn't matter whether it was handled in an earlier call to discover_region(); we recognize both marker objects and strings here.)
                perimeter += 1
    return area, perimeter


def generate_costs(level_map):
    w, h = len(level_map[0]), len(level_map)
    for y in range(h):
        for x in range(w):
            # print(f"{level_map[y][x]} has ", end="")
            area, perimeter = discover_region(level_map, x, y)
            # print(f"{area=}, {perimeter=}, {area * perimeter=}")
            yield area * perimeter


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    level_map = [list(line) for line in data.split("\n")]
    costs = list(generate_costs(level_map))
    print(f"{costs=}")
    print(f"{sum(costs)=}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
