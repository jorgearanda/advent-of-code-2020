#!/usr/bin/env python3


class ConwayCube:
    def count_live(self):
        return len(self.live)

    def get_ranges(self, dimension):
        return (
            min([coords[dimension] for coords in self.live]),
            max([coords[dimension] for coords in self.live]),
        )


class ConwayCube3D(ConwayCube):
    def __init__(self, input_lines):
        self.live = {}
        for y, line in enumerate(input_lines):
            for x, cell in enumerate(line):
                if cell == "#":
                    self.live[(x, y, 0)] = True

    def show(self):
        min_x, max_x = self.get_ranges(0)
        min_y, max_y = self.get_ranges(1)
        min_z, max_z = self.get_ranges(2)
        for k in range(min_z, max_z + 1):
            print(f"z={k}")
            for j in range(min_y, max_y + 1):
                line = ""
                for i in range(min_x, max_x + 1):
                    line += "#" if self.live.get((i, j, k)) else "."
                print(f"{line}")
            print()

    def cycle(self):
        new_live = {}
        min_x, max_x = self.get_ranges(0)
        min_y, max_y = self.get_ranges(1)
        min_z, max_z = self.get_ranges(2)
        for i in range(min_x - 1, max_x + 2):
            for j in range(min_y - 1, max_y + 2):
                for k in range(min_z - 1, max_z + 2):
                    live_cells = self.live_cells_around((i, j, k))
                    if self.live.get((i, j, k)) and 3 <= live_cells <= 4:
                        new_live[(i, j, k)] = True
                    if not self.live.get((i, j, k)) and live_cells == 3:
                        new_live[(i, j, k)] = True
        self.live = new_live
        return self.count_live()

    def live_cells_around(self, coords):
        x, y, z = coords
        live_cells = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                for k in range(z - 1, z + 2):
                    if self.live.get((i, j, k)):
                        live_cells += 1
        return live_cells


class ConwayCube4D(ConwayCube):
    def __init__(self, input_lines):
        self.live = {}
        for y, line in enumerate(input_lines):
            for x, cell in enumerate(line):
                if cell == "#":
                    self.live[(x, y, 0, 0)] = True

    def cycle(self):
        new_live = {}
        min_x, max_x = self.get_ranges(0)
        min_y, max_y = self.get_ranges(1)
        min_z, max_z = self.get_ranges(2)
        min_w, max_w = self.get_ranges(3)
        for i in range(min_x - 1, max_x + 2):
            for j in range(min_y - 1, max_y + 2):
                for k in range(min_z - 1, max_z + 2):
                    for l in range(min_w - 1, max_w + 2):
                        live_cells = self.live_cells_around((i, j, k, l))
                        if self.live.get((i, j, k, l)) and 3 <= live_cells <= 4:
                            new_live[(i, j, k, l)] = True
                        if not self.live.get((i, j, k, l)) and live_cells == 3:
                            new_live[(i, j, k, l)] = True
        self.live = new_live
        return self.count_live()

    def live_cells_around(self, coords):
        x, y, z, w = coords
        live_cells = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                for k in range(z - 1, z + 2):
                    for l in range(w - 1, w + 2):
                        if self.live.get((i, j, k, l)):
                            live_cells += 1
        return live_cells


def load_input(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


if __name__ == "__main__":
    c = ConwayCube3D(load_input("day17_input.txt"))
    for _ in range(6):
        c.cycle()
    print(f"Part 1: {c.count_live()}")
    c = ConwayCube4D(load_input("day17_input.txt"))
    for _ in range(6):
        c.cycle()
    print(f"Part 2: {c.count_live()}")


# ~~~ Tests ~~~ #


def test_six_cycle_3d():
    c = ConwayCube3D([".#.", "..#", "###"])
    for _ in range(6):
        c.cycle()
    assert c.count_live() == 112


def test_six_cycle_4d():
    c = ConwayCube4D([".#.", "..#", "###"])
    for _ in range(6):
        c.cycle()
    assert c.count_live() == 848
