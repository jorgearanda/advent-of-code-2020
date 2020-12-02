#!/usr/bin/env python3


class Password:
    def __init__(self, password_line):
        line_bits = password_line.split()
        limits = line_bits[0].split("-")
        self.low = int(limits[0])
        self.high = int(limits[1])
        self.must_contain = line_bits[1][0]
        self.password = line_bits[2]

    def valid_by_letter_appearances(self):
        return self.low <= self.password.count(self.must_contain) <= self.high

    def valid_by_appearance_at_index(self):
        return bool(self.password[self.low - 1] == self.must_contain) ^ bool(
            self.password[self.high - 1] == self.must_contain
        )

    def valid(self, method):
        if method == 1:
            return self.valid_by_letter_appearances()
        else:
            return self.valid_by_appearance_at_index()


def load_input(filename):
    with open(filename) as f:
        return [Password(line) for line in f.readlines()]


def valid_passwords(passwords, method=1):
    return sum(1 for password in passwords if password.valid(method))


if __name__ == "__main__":
    passwords = load_input("day02_input.txt")
    print(f"Part 1: {valid_passwords(passwords, method=1)}")
    print(f"Part 1: {valid_passwords(passwords, method=2)}")


def test_password_init():
    p = Password("1-3 a: abcde")
    assert p.low == 1
    assert p.high == 3
    assert p.must_contain == "a"
    assert p.password == "abcde"


def test_password_valid_method_1():
    assert Password("1-3 a: abcde").valid(method=1)
    assert Password("2-9 c: ccccccccc").valid(method=1)
    assert not Password("1-3 b: cdefg").valid(method=1)


def test_password_valid_method_2():
    assert Password("1-3 a: abcde").valid(method=2)
    assert not Password("2-9 c: ccccccccc").valid(method=2)
    assert not Password("1-3 b: cdefg").valid(method=2)


def test_valid_password_count():
    ps = [
        Password("1-3 a: abcde"),
        Password("1-3 b: cdefg"),
        Password("2-9 c: ccccccccc"),
    ]
    assert valid_passwords(ps, method=1) == 2
