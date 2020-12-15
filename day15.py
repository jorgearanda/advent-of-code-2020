#!/usr/bin/env python3


class Game:
    def __init__(self, seed):
        self.turn = 1
        self.last_spoken = {}
        for item in seed:
            self.last_spoken[item] = (self.turn, 0)
            self.turn += 1
            self.last_number_spoken = item

    def turns_since_last_spoken(self, item):
        if item in self.last_spoken:
            return self.turn - self.last_spoken[item][1]
        else:
            return 0

    def speak(self):
        if self.last_spoken[self.last_number_spoken][1] == 0:
            next_number_spoken = 0
        else:
            next_number_spoken = (
                self.last_spoken[self.last_number_spoken][0]
                - self.last_spoken[self.last_number_spoken][1]
            )
        if next_number_spoken in self.last_spoken:
            self.last_spoken[next_number_spoken] = (
                self.turn,
                self.last_spoken[next_number_spoken][0],
            )
        else:
            self.last_spoken[next_number_spoken] = (self.turn, 0)
        self.turn += 1
        self.last_number_spoken = next_number_spoken

    def speak_until(self, limit):
        while self.turn <= limit:
            self.speak()
        return self.last_number_spoken


if __name__ == "__main__":
    g = Game([7, 12, 1, 0, 16, 2])
    print(f"Part 1: {g.speak_until(2020)}")
    print(f"Part 2: {g.speak_until(30_000_000)}")

# ~~~ Tests ~~~ #


def test_speak_until():
    g = Game([0, 3, 6])
    assert g.speak_until(2020) == 436
