#!/usr/bin/env python3

# This won't work if the input is transitive, e.g. if "X|Y" and "Y|Z" is given, then "Z,X" would be considered "ordered".
# Treat all numbers as strings because whatever.

from collections import defaultdict
import sys


def parse_orders(orders_raw):
    forbidden_earlier = defaultdict(set)
    for line in orders_raw.split("\n"):
        page_early, page_late = line.strip().split("|")
        forbidden_earlier[page_early].add(page_late)
    return forbidden_earlier


def parse_books(books_raw):
    books = []
    for line in books_raw.split("\n"):
        books.append(line.split(","))
    return books


def is_ordered(book, forbidden_earlier):
    seen_pages = set()
    for page in book:
        if forbidden_earlier[page].intersection(seen_pages):
            return False
        seen_pages.add(page)
    return True


def run(filename):
    with open(filename, "r") as fp:
        data = fp.read().strip()
    orders_raw, books_raw = data.split("\n\n")
    forbidden_later = parse_orders(orders_raw.strip())
    books = parse_books(books_raw.strip())
    acc = 0
    for book in books:
        if is_ordered(book, forbidden_later):
            acc += int(book[len(book) // 2])
    print(acc)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run("real.txt")
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} [/path/to/input.txt]", file=sys.stderr)
        exit(1)
