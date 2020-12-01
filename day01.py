from itertools import combinations

SUM_TO = 2020


def load_input(filename):
    with open(filename) as f:
        return [int(line) for line in f.readlines()]


def find_two_entry_product(report):
    for entry in report:
        if SUM_TO - entry in report:
            return entry * (SUM_TO - entry)


def find_three_entry_product(report):
    for entry1, entry2 in combinations(report, 2):
        if SUM_TO - entry1 - entry2 in report:
            return entry1 * entry2 * (SUM_TO - entry1 - entry2)


if __name__ == "__main__":
    report = load_input("day01_input.txt")
    print(f"Part 1: {find_two_entry_product(report)}")
    print(f"Part 2: {find_three_entry_product(report)}")


def test_sample_part_1():
    report = [1721, 979, 366, 299, 675, 1456]
    assert find_two_entry_product(report) == 514579


def test_sample_part_2():
    report = [1721, 979, 366, 299, 675, 1456]
    assert find_three_entry_product(report) == 241861950
