#!/usr/bin/env python3


class Ferry:
    def __init__(self, instructions, waypoint=False):
        self.x = 0
        self.y = 0
        self.facing = 0
        self.waypoint_x = 10
        self.waypoint_y = 1
        for instruction in instructions:
            if not waypoint:
                self.move(instruction)
            else:
                self.move_with_waypoint(instruction)

    def move(self, instruction):
        command = instruction[0]
        amount = int(instruction[1:])
        if command == "F":
            if self.facing == 0:
                command = "E"
            elif self.facing == 90:
                command = "N"
            elif self.facing == 180:
                command = "W"
            elif self.facing == 270:
                command = "S"
            else:
                print(f"Unexpected facing: {self.facing}")
        if command == "N":
            self.y += amount
        elif command == "S":
            self.y -= amount
        elif command == "E":
            self.x += amount
        elif command == "W":
            self.x -= amount
        elif command == "L":
            self.facing = (self.facing + amount) % 360
        elif command == "R":
            self.facing = (36000 + self.facing - amount) % 360
        else:
            print(f"Unexpected command: {command}")

    def move_with_waypoint(self, instruction):
        command = instruction[0]
        amount = int(instruction[1:])
        if command == "F":
            self.x += self.waypoint_x * amount
            self.y += self.waypoint_y * amount
        elif command == "N":
            self.waypoint_y += amount
        elif command == "S":
            self.waypoint_y -= amount
        elif command == "E":
            self.waypoint_x += amount
        elif command == "W":
            self.waypoint_x -= amount
        elif command == "L":
            turns = amount // 90
            for _ in range(turns):
                self.waypoint_x, self.waypoint_y = self.waypoint_y * -1, self.waypoint_x
        elif command == "R":
            turns = amount // 90
            for _ in range(turns):
                self.waypoint_x, self.waypoint_y = self.waypoint_y, self.waypoint_x * -1
        else:
            print(f"Unexpected command: {command}")

    def distance_from_origin(self):
        return abs(self.x) + abs(self.y)


def load_input(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


if __name__ == "__main__":
    instructions = load_input("day12_input.txt")
    ferry = Ferry(instructions)
    print(f"Part 1: {ferry.distance_from_origin()}")
    ferry = Ferry(instructions, waypoint=True)
    print(f"Part 2: {ferry.distance_from_origin()}")

# ~~~ Tests ~~~ #


def test_distance():
    instructions = ["F10", "N3", "F7", "R90", "F11"]
    ferry = Ferry(instructions)
    assert ferry.distance_from_origin() == 25


def test_distance_with_waypoint():
    instructions = ["F10", "N3", "F7", "R90", "F11"]
    ferry = Ferry(instructions, waypoint=True)
    assert ferry.distance_from_origin() == 286
