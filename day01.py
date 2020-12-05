#!/usr/bin/env python3

from itertools import combinations
from math import prod

SUM_TO = 2020


def load_input(filename):
    with open(filename) as f:
        return [int(line) for line in f.readlines()]


def find_match_product(report, items):
    for combination in combinations(report, items):
        if sum(combination) == SUM_TO:
            return prod(combination)


if __name__ == "__main__":
    report = load_input("day01_input.txt")
    print(f"Part 1: {find_match_product(report, 2)}")
    print(f"Part 2: {find_match_product(report, 3)}")


# ~~~ Tests ~~~ #


def test_sample_part_1():
    report = [1721, 979, 366, 299, 675, 1456]
    assert find_match_product(report, 2) == 514579


def test_sample_part_2():
    report = [1721, 979, 366, 299, 675, 1456]
    assert find_match_product(report, 3) == 241861950
