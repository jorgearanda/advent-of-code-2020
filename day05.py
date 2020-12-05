#!/usr/bin/env python3

BACKS = [64, 32, 16, 8, 4, 2, 1]
RIGHTS = [4, 2, 1]


class BoardingPass:
    def __init__(self, code):
        self.row = sum([BACKS[i] for i, val in enumerate(code[:7]) if val == "B"])
        self.col = sum([RIGHTS[i] for i, val in enumerate(code[7:]) if val == "R"])
        self.seat_id = self.row * 8 + self.col


def highest_seat_id(boarding_passes):
    return max(boarding_passes, key=lambda x: x.seat_id).seat_id


def missing_seat_id(boarding_passes):
    boarding_passes.sort(key=lambda x: x.seat_id)
    cursor_bp = boarding_passes[0].seat_id
    for bp in boarding_passes[1:]:
        if bp.seat_id != cursor_bp + 1:
            return cursor_bp + 1
        cursor_bp += 1


def load_input(filename):
    with open(filename) as f:
        return f.readlines()


if __name__ == "__main__":
    bp_lines = load_input("day05_input.txt")
    bps = [BoardingPass(line.strip()) for line in bp_lines]
    print(f"Part 1: {highest_seat_id(bps)}")
    print(f"Part 2: {missing_seat_id(bps)}")


# ~~~ Tests ~~~ #


def test_seat_decoding():
    bp = BoardingPass("FBFBBFFRLR")
    assert bp.row == 44
    assert bp.col == 5
    assert bp.seat_id == 357

    assert BoardingPass("BFFFBBFRRR").seat_id == 567
    assert BoardingPass("FFFBBBFRRR").seat_id == 119
    assert BoardingPass("BBFFBBFRLL").seat_id == 820


def test_highest_seat_id():
    assert (
        highest_seat_id(
            [
                BoardingPass("FBFBBFFRLR"),
                BoardingPass("BFFFBBFRRR"),
                BoardingPass("FFFBBBFRRR"),
                BoardingPass("BBFFBBFRLL"),
            ]
        )
        == 820
    )


def test_missing_seat_id():
    assert (
        missing_seat_id(
            [
                BoardingPass("FFFBBBFRRR"),  # 119
                BoardingPass("FFFBBBFRRL"),  # 118
                BoardingPass("FFFBBBFRLR"),  # 117
                BoardingPass("FFFBBBBLLR"),  # 121
            ]
        )
        == 120
    )
