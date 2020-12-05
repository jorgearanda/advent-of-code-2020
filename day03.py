#!/usr/bin/env python3

from math import prod

OPEN = "."
TREE = "#"
OUT = None


class Map:
    def __init__(self, input):
        self.pattern = input
        self.rows = len(self.pattern)
        self.cols = len(self.pattern[0])
        self.location = (1, 1)

    def at(self, col, row):
        if row > self.rows:
            return OUT
        return self.pattern[row - 1][col % self.cols - 1]

    def at_location(self):
        return self.at(*self.location)

    def step(self, cols, rows):
        self.location = (self.location[0] + cols, self.location[1] + rows)
        return self.at_location()

    def trees_until_out(self, cols, rows):
        trees = 0
        self.location = (1, 1)
        while True:
            next_step = self.step(cols, rows)
            if next_step == TREE:
                trees += 1
            elif next_step == OUT:
                break
        return trees

    def trees_product(self, slopes):
        return prod([self.trees_until_out(*slope) for slope in slopes])


def load_input(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


if __name__ == "__main__":
    map = Map(load_input("day03_input.txt"))
    print(f"Part 1: {map.trees_until_out(3, 1)}")
    print(f"Part 2: {map.trees_product([(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)])}")


# ~~~ Tests ~~~ #


TEST_INPUT = [
    "..##.......",
    "#...#...#..",
    ".#....#..#.",
    "..#.#...#.#",
    ".#...##..#.",
    "..#.##.....",
    ".#.#.#....#",
    ".#........#",
    "#.##...#...",
    "#...##....#",
    ".#..#...#.#",
]


def test_map_coords():
    map = Map(TEST_INPUT)
    assert map.at(1, 1) == OPEN
    assert map.at(3, 1) == TREE
    assert map.at(1, 2) == TREE
    assert map.at(12, 2) == TREE
    assert map.at(23, 2) == TREE
    assert map.at(1, 12) == OUT
    assert map.at_location() == OPEN
    assert map.step(3, 1) == OPEN


def test_trees_until_out():
    map = Map(TEST_INPUT)
    assert map.trees_until_out(3, 1) == 7


def test_trees_product():
    map = Map(TEST_INPUT)
    assert map.trees_product([(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]) == 336
