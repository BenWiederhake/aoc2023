#!/usr/bin/env python3

import sys


def gen_reports(data):
    for line in data.split("\n"):
        yield [int(number) for number in line.split(" ")]


def is_okay(level, last_level, allowed):
    assert level is not None
    return last_level is None or level - last_level in allowed


def is_allowed(report, allowed):
    second_last_level = None
    last_level = None
    skipped = False
    either_is_okay = False
    for level in report:
        if is_okay(level, last_level, allowed):
            second_last_level = last_level
            last_level = level
            either_is_okay = False
            continue
        if either_is_okay:
            assert skipped
            if is_okay(level, second_last_level, allowed):
                # Retroactively make it so that "last_level" is skipped.
                # Intentionally don't update second_last_level, although it doesn't matter anymore.
                last_level = level
                either_is_okay = False
                continue
        if skipped:
            # Nah, this is broken / "unsafe".
            return False
        skipped = True
        # Need to skip something. But which? Last level, or this level?
        if not is_okay(level, second_last_level, allowed):
            # Definitely *this* level!
            # Intentionally don't update last_level or second_last_level.
            assert not either_is_okay
            continue
        # Still not sure which one to skip. Let the next step decide, if there even is one.
        second_last_level = last_level
        last_level = level
        either_is_okay = True
    return True


def is_safe(report):
    return is_allowed(report, (1, 2, 3)) or is_allowed(report, (-1, -2, -3))


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    for report in gen_reports(data):
        if not is_safe(report):
            print(f"unsafe?: {report}")
    num_safe = sum(is_safe(report) for report in gen_reports(data))
    print(num_safe)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
