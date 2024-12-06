#!/usr/bin/env python3

# This won't work if the input is transitive, e.g. if "X|Y" and "Y|Z" is given, then "Z,X" would be considered "ordered".
# Treat all numbers as strings because whatever.

from collections import defaultdict
import sys


def parse_orders(orders_raw):
    earlier = defaultdict(set)
    for line in orders_raw.split("\n"):
        page_early, page_late = line.strip().split("|")
        earlier[page_late].add(page_early)
    return earlier


def parse_books(books_raw):
    books = []
    for line in books_raw.split("\n"):
        books.append(line.split(","))
    return books


def order_book(book, earlier):
    remaining = set(book)
    ordered_book = []
    while remaining:
        e = remaining.pop()
        # print(f"{len(remaining)} candidates")
        while True:
            conflicts = earlier[e].intersection(remaining)
            # print(f"  [{e}] -> {len(conflicts)} conflicts: {conflicts}")
            if conflicts:
                # "e" must not be the next element. Instead, try one of the conflicting elements:
                e2 = conflicts.pop()
                remaining.add(e)
                remaining.remove(e2)
                e = e2
            else:
                # Hooray! "e" could be the next one in the order.
                ordered_book.append(e)
                break
    return ordered_book


def ordered_center(book, earlier):
    book_ordered = order_book(book, earlier)
    if book != book_ordered:
        return int(book_ordered[len(book_ordered) // 2])
    return 0


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    orders_raw, books_raw = data.split("\n\n")
    earlier = parse_orders(orders_raw.strip())
    books = parse_books(books_raw.strip())
    acc = 0
    for book in books:
        acc += ordered_center(book, earlier)
    print(acc)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("real.txt")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
