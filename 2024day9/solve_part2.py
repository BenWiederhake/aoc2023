#!/usr/bin/env python3

import sys

FILE_NONE = -1


def make_file_blocks(fs_map):
    generating = 0
    file_blocks = []
    file_meta = []
    for region_length in fs_map:
        region_length = int(region_length)
        if generating != FILE_NONE:
            file_meta.append((len(file_blocks), region_length))
        for _ in range(region_length):
            file_blocks.append(generating)
        if generating != FILE_NONE:
            generating = FILE_NONE
        else:
            generating = len(file_meta)
    return file_blocks, file_meta


def compact_file_blocks_inplace(file_blocks, file_meta):
    for file_id in range(len(file_meta) - 1, 0 - 1, -1):
        file_pos, file_len = file_meta[file_id]
        # Note: We can't do anything like early stopping, because it might that e.g. file 1 has size 1,
        # there's a 1-sized gap between file 0 and file 1, and all the other files are size 2 or larger.
        # Note: As demonstrated by file 8 in the example, a file does not move if the new area overlaps with the old area.
        # Check for destination candidates:
        for after_file_id, (after_file_pos, after_file_len) in enumerate(file_meta):
            if after_file_id == file_id:
                # The file itself.
                # Later files, or a files that might have already moved, are irrelevant anyway.
                break
            assert after_file_id < file_id
            after_after_file_pos, _after_after_file_len = file_meta[after_file_id + 1]
            # FIXME: This assumes that _after_after_file_len is at least 1!
            # In practice, this seems to hold true.
            after_file_free_space = after_after_file_pos - (after_file_pos + after_file_len)
            if after_file_free_space < file_len:
                # It's not even plausible to insert the current file there, no matter whether anything moved into that gap in the meantime!
                continue
            # So it is plausible; but still not guaranteed. Check for the actual free space.
            # Note that there might be a few new files in the way that need to be skipped.
            after_file_free_space_actual = sum(fb == FILE_NONE for fb in file_blocks[after_file_pos + after_file_len : after_after_file_pos])
            assert after_file_free_space_actual <= after_file_free_space
            if after_file_free_space_actual < file_len:
                # Nope, can't actually put it here.
                continue
            # Note that all the "new files in the way" must be left-aligned, so if there is any free space,
            # then it must be contiguous and on the right side.
            after_file_free_space_pos = after_after_file_pos - after_file_free_space_actual
            assert after_file_free_space_pos + file_len <= file_pos
            # Finally, actually carry out the move:
            for i in range(file_len):
                file_blocks[file_pos + i] = FILE_NONE
                file_blocks[after_file_free_space_pos + i] = file_id
            # Probably don't need to update, but just for fun:
            file_meta[file_id] = (after_file_free_space_pos, file_len)
            # No need to check additional places further right.
            break
    # This algorithm feels overly complicated. What's a simpler solution?


def run(filename):
    with open(filename, "r") as fp:
        fs_map = fp.read().strip()
    assert len(fs_map) % 2 == 1, f"not odd?! {len(fs_map)=}"
    # Create the file_blocks map, and also note down which file starts where and is how long:
    file_blocks, file_meta = make_file_blocks(fs_map)
    compact_file_blocks_inplace(file_blocks, file_meta)
    # print(file_blocks)
    # print(file_meta)
    checksum = sum(i * file_id for i, file_id in enumerate(file_blocks) if file_id != FILE_NONE)
    print(f"{checksum=}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("input")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
