#!/usr/bin/env python3

import math
import sys


class ResolvableValue:
    def __init__(self, value_start, value_len):
        assert value_len > 0
        self.current_start = value_start
        self.current_len = value_len
        self.is_mapped = False

    def consider_mapping(self, dst_start, src_start, length):
        if self.is_mapped:
            return [self]
        current_end = self.current_start + self.current_len
        src_end = src_start + length
        if current_end <= src_start or self.current_start >= src_end:
            # Does not apply
            return [self]
        elif src_start == dst_start:
            print(f"lolwut, {src_start=} == {dst_start}?!")
            # Shortcut:
            self.is_mapped = True
            return [self]
        else:
            oldstate = self.__repr__()
            oldlen = self.current_len
            results = [self]
            # print(f"{oldstate} | [{dst_start} {src_start} {length}] → …")
            if self.current_start < src_start:
                # There is a section BEFORE src_start that isn't actually mapped; split it off:
                before = ResolvableValue(self.current_start, src_start - self.current_start)
                # Intentionally leave is_mapped=False
                results.append(before)
                self.current_len -= src_start - self.current_start
                assert self.current_len > 0
                self.current_start = src_start
                assert oldlen == sum(s.current_len for s in results), results
            if current_end > src_end:
                # There is a section AFTER src_start that isn't actually mapped; split it off:
                after = ResolvableValue(src_end, current_end - src_end)
                # Intentionally leave is_mapped=False
                results.append(after)
                self.current_len -= current_end - src_end
                assert self.current_len > 0
                current_end = src_end
                assert oldlen == sum(s.current_len for s in results), results
            # Now that we're certain that self is fully contained inside [src_start, src_end), we can just add the offset:
            self.current_start += dst_start - src_start
            self.is_mapped = True
            # print(f"{oldstate} | [{dst_start} {src_start} {length}] → {results}")
            assert oldlen == sum(s.current_len for s in results)
            return results
        raise AssertionError()

    def commit(self):
        self.is_mapped = False

    def __repr__(self):
        return f"R[{self.current_start}+{self.current_len}{'UM'[self.is_mapped]}]"


def solve(lines):
    assert len(lines) > 10, lines
    seed_parts = lines[0].split()
    assert seed_parts[0] == "seeds:"
    assert len(seed_parts) % 2 == 1
    seeds = []
    for i in range(len(seed_parts) // 2):
        range_start = int(seed_parts[i * 2 + 1])
        range_len = int(seed_parts[i * 2 + 2])
        seeds.append(ResolvableValue(int(range_start), int(range_len)))
    assert lines[1] == ""

    for i, line in enumerate(lines[2 :]):
        if line.endswith(" map:"):
            # print(f"After previous map: {seeds}")
            # print(f"Now doing {line}")
            continue
        if not line:
            for seed in seeds:
                seed.commit()
            continue
        parts = line.split()
        assert len(parts) == 3, (i + 2, line)
        dst_start = int(parts[0])
        src_start = int(parts[1])
        length = int(parts[2])
        # There's a cleverer way to iterate only over those seeds that are likely to change, but that's too much work.
        seeds = sum((seed.consider_mapping(dst_start, src_start, length) for seed in seeds), [])
    print(f"{len(seeds)=} {seeds=}")
    # Hack: Even though each seed object technically represents a range,
    # we search for the minimum value anyway, so current_start is
    # the only candidate for each object.
    return min(seed.current_start for seed in seeds)


def as_lines(data):
    lines = data.split("\n")
    # No cleanup necessary! Trailing emptyline doesn't matter.
    return lines


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read()
    lines = as_lines(data)
    solution = solve(lines)
    print(solution)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("real.txt")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
