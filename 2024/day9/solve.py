#!/usr/bin/env python3

import sys


def generate_compacted_blocks(fs_map):
    fs_map = [int(d) for d in fs_map]  # make it mutable, convert to int
    file_id_offset = 0
    fs_offset = 0
    while True:
        if fs_map[0] == 0:
            print("0-sized file!")
        # First, handle all the contiguous file blocks:
        for _ in range(fs_map[0]):
            yield file_id_offset
        fs_map[0] = 0
        if len(fs_map) == 1:
            # Nothing left to do!
            return
        # Then, handle as much space from the back as possible:
        while fs_map[1] > 0:
            last_file_block_count = fs_map[-1]
            if last_file_block_count == 0:
                # Remove the empty file (and space before it):
                fs_map = fs_map[: -2]
                assert len(fs_map) % 2 == 1
                if len(fs_map) == 1:
                    # No remaining blocks, great!
                    assert fs_map == [0]
                    return
            else:
                # Steal one block from it:
                yield file_id_offset + len(fs_map) // 2
                fs_map[1] -= 1
                fs_map[-1] -= 1
        assert len(fs_map) >= 3
        # Finally, we're done with the current position (file blocks and free space are used up).
        fs_map = fs_map[2 :]
        file_id_offset += 1


def run(filename):
    with open(filename, "r") as fp:
        fs_map = fp.read().strip()
    assert len(fs_map) % 2 == 1, f"not odd?! {len(fs_map)=}"
    # for i, file_id in enumerate(generate_compacted_blocks(fs_map)):
    #     print(f"{file_id},", end="")
    # print()
    checksum = sum(i * file_id for i, file_id in enumerate(generate_compacted_blocks(fs_map)))
    print(f"{checksum=}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
