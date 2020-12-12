#!/usr/bin/env python3


class Layout:
    def __init__(self, layout_text, method="adjacent"):
        self.rows = []
        self.equilibrium = False
        self.ticks = 0
        self.method = method
        for row in layout_text:
            self.rows.append([x for x in row.strip()])

    def show(self):
        print(f"Ticks: {self.ticks}")
        print(f"Occupied: {self.occupied()}")
        for j in range(len(self.rows)):
            print((str(j) + ":  ")[:4] + "".join(self.rows[j]))
        print("\n")

    def tick(self):
        new_rows = []
        for _ in range(len(self.rows)):
            new_rows.append(["."] * len(self.rows[0]))
        for j in range(len(self.rows)):
            for i in range(len(self.rows[0])):
                if self.rows[j][i] == ".":
                    continue
                elif self.rows[j][i] == "L":
                    if self.empty_around(j, i):
                        new_rows[j][i] = "#"
                    else:
                        new_rows[j][i] = "L"
                else:
                    if self.crowded_around(j, i):
                        new_rows[j][i] = "L"
                    else:
                        new_rows[j][i] = "#"
        for j in range(len(self.rows)):
            if "".join(self.rows[j]) != "".join(new_rows[j]):
                self.equilibrium = False
                break
        else:
            self.equilibrium = True
        self.rows = new_rows
        self.ticks += 1

    def occupied_neighbour_seats(self, j, i):
        occupied = 0
        # Row above
        if j > 0:
            if i > 0:
                if self.rows[j - 1][i - 1] == "#":
                    occupied += 1
            if self.rows[j - 1][i] == "#":
                occupied += 1
            if i < len(self.rows[0]) - 1:
                if self.rows[j - 1][i + 1] == "#":
                    occupied += 1

        # Same row
        if i > 0:
            if self.rows[j][i - 1] == "#":
                occupied += 1
        if i < len(self.rows[0]) - 1:
            if self.rows[j][i + 1] == "#":
                occupied += 1

        # Row below
        if j < len(self.rows) - 1:
            if i > 0:
                if self.rows[j + 1][i - 1] == "#":
                    occupied += 1
            if self.rows[j + 1][i] == "#":
                occupied += 1
            if i < len(self.rows[0]) - 1:
                if self.rows[j + 1][i + 1] == "#":
                    occupied += 1

        return occupied

    def occupied_line_of_sight_seats(self, j, i):
        occupied = 0
        cur_j = j - 1
        cur_i = i - 1
        while cur_j >= 0 and cur_i >= 0:
            if self.rows[cur_j][cur_i] == "#":
                occupied += 1
                break
            if self.rows[cur_j][cur_i] == "L":
                break
            cur_j -= 1
            cur_i -= 1

        cur_j = j - 1
        cur_i = i
        while cur_j >= 0:
            if self.rows[cur_j][cur_i] == "#":
                occupied += 1
                break
            if self.rows[cur_j][cur_i] == "L":
                break
            cur_j -= 1

        cur_j = j - 1
        cur_i = i + 1
        while cur_j >= 0 and cur_i < len(self.rows[0]):
            if self.rows[cur_j][cur_i] == "#":
                occupied += 1
                break
            if self.rows[cur_j][cur_i] == "L":
                break
            cur_j -= 1
            cur_i += 1

        cur_j = j
        cur_i = i - 1
        while cur_i >= 0:
            if self.rows[cur_j][cur_i] == "#":
                occupied += 1
                break
            if self.rows[cur_j][cur_i] == "L":
                break
            cur_i -= 1

        cur_j = j
        cur_i = i + 1
        while cur_i < len(self.rows[0]):
            if self.rows[cur_j][cur_i] == "#":
                occupied += 1
                break
            if self.rows[cur_j][cur_i] == "L":
                break
            cur_i += 1

        cur_j = j + 1
        cur_i = i - 1
        while cur_j < len(self.rows) and cur_i >= 0:
            if self.rows[cur_j][cur_i] == "#":
                occupied += 1
                break
            if self.rows[cur_j][cur_i] == "L":
                break
            cur_j += 1
            cur_i -= 1

        cur_j = j + 1
        cur_i = i
        while cur_j < len(self.rows):
            if self.rows[cur_j][cur_i] == "#":
                occupied += 1
                break
            if self.rows[cur_j][cur_i] == "L":
                break
            cur_j += 1

        cur_j = j + 1
        cur_i = i + 1
        while cur_j < len(self.rows) and cur_i < len(self.rows[0]):
            if self.rows[cur_j][cur_i] == "#":
                occupied += 1
                break
            if self.rows[cur_j][cur_i] == "L":
                break
            cur_j += 1
            cur_i += 1

        return occupied

    def empty_around(self, j, i):
        if self.method == "adjacent":
            return self.occupied_neighbour_seats(j, i) == 0
        else:
            return self.occupied_line_of_sight_seats(j, i) == 0

    def crowded_around(self, j, i):
        if self.method == "adjacent":
            return self.occupied_neighbour_seats(j, i) >= 4
        else:
            return self.occupied_line_of_sight_seats(j, i) >= 5

    def occupied(self):
        total = 0
        for row in self.rows:
            total += "".join(row).count("#")
        return total

    def occupied_on_equilibrium(self):
        while not self.equilibrium:
            self.tick()
        return self.occupied()


def load_input(filename):
    with open(filename) as f:
        return f.readlines()


if __name__ == "__main__":
    layout = Layout(load_input("day11_input.txt"))
    print(f"Part 1: {layout.occupied_on_equilibrium()}")
    layout = Layout(load_input("day11_input.txt"), method="line of sight")
    print(f"Part 2: {layout.occupied_on_equilibrium()}")


# ~~~ Tests ~~~ #

TEST_LAYOUT = """
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""


def test_first_round():
    layout = Layout(TEST_LAYOUT.split("\n")[1:-1])
    layout.tick()
    assert "".join(layout.rows[0]) == "#.##.##.##"
    assert not layout.equilibrium


def test_equilibrium():
    layout = Layout(TEST_LAYOUT.split("\n")[1:-1])
    assert layout.occupied_on_equilibrium() == 37


def test_small():
    layout = Layout(["LLL", "LLL", "LLL"])
    layout.tick()
    assert "".join(layout.rows[0]) == "###"
    assert "".join(layout.rows[1]) == "###"
    assert "".join(layout.rows[2]) == "###"
    layout.tick()
    assert "".join(layout.rows[0]) == "#L#"
    assert "".join(layout.rows[1]) == "LLL"
    assert "".join(layout.rows[2]) == "#L#"
    layout.tick()
    assert "".join(layout.rows[0]) == "#L#"
    assert "".join(layout.rows[1]) == "LLL"
    assert "".join(layout.rows[2]) == "#L#"


def test_equilibrium_line_of_sight():
    layout = Layout(TEST_LAYOUT.split("\n")[1:-1], method="line of sight")
    assert layout.occupied_on_equilibrium() == 26
