#!/usr/bin/env python3

from collections import deque


class DataStream:
    def __init__(self, preamble):
        self.window = deque([], preamble)

    def add_valid(self, value):
        if len(self.window) < self.window.maxlen:
            self.window.append(value)
            return True

        for item in self.window:
            if value - item in self.window and value % item != 0:
                self.window.append(value)
                return True

        return False


def find_invalid(preamble, items):
    ds = DataStream(preamble)
    for item in items:
        item = int(item)
        if ds.add_valid(item) is False:
            return item


def find_min_max_in_sequence(value, items):
    items = [int(item) for item in items]
    for start in range(len(items)):
        for end in range(start + 1, len(items)):
            if sum(items[start:end]) == value:
                return min(items[start:end]) + max(items[start:end])
            elif sum(items[start:end]) > value:
                break


def load_input(filename):
    with open(filename) as f:
        return f.readlines()


if __name__ == "__main__":
    items = load_input("day09_input.txt")
    invalid = find_invalid(25, items)
    print(f"Part 1: {invalid}")
    print(f"Part 2: {find_min_max_in_sequence(invalid, items)}")


# ~~~ Tests ~~~ #


TEST_STREAM = "35\n20\n15\n25\n47\n40\n62\n55\n65\n95\n102\n117\n150\n182\n127\n219\n299\n277\n309\n576"


def test_find_invalid():
    assert find_invalid(5, TEST_STREAM.split("\n")) == 127


def test_find_min_max_in_sequence():
    assert find_min_max_in_sequence(127, TEST_STREAM.split("\n")) == 62
