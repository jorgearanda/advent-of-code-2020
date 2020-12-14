#!/usr/bin/env python3

from itertools import product


class Memory:
    def __init__(self):
        self.memory = {}

    def process_instruction(self, instruction):
        command, value = instruction.split(" = ")
        if command == "mask":
            self.set_mask(value)
        else:
            self.set_value(int(command[4:-1]), int(value))

    def process_instructions(self, instructions):
        for instruction in instructions:
            self.process_instruction(instruction)

    def memory_sum(self):
        return sum(value for value in self.memory.values())


class MemoryV1(Memory):
    def set_mask(self, mask):
        self.mask0 = int(mask.replace("X", "1"), 2)
        self.mask1 = int(mask.replace("X", "0"), 2)

    def set_value(self, address, value):
        self.memory[address] = value & self.mask0 | self.mask1


class MemoryV2(Memory):
    def set_mask(self, mask):
        self.mask = mask

    def set_value(self, address, value):
        address = address | int(self.mask.replace("X", "0"), 2)
        address = format(address, "036b")
        for i in range(len(self.mask)):
            if self.mask[i] == "X":
                address = address[:i] + "X" + address[i + 1 :]
        for combination in product("01", repeat=address.count("X")):
            sub_i = 0
            float_address = address
            for i in range(len(address)):
                if float_address[i] == "X":
                    float_address = (
                        float_address[:i] + combination[sub_i] + float_address[i + 1 :]
                    )
                    sub_i += 1
            self.memory[float_address] = value


def load_input(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


if __name__ == "__main__":
    instructions = load_input("day14_input.txt")
    m = MemoryV1()
    m.process_instructions(instructions)
    print(f"Part 1: {m.memory_sum()}")
    m = MemoryV2()
    m.process_instructions(instructions)
    print(f"Part 2: {m.memory_sum()}")


# ~~~ Tests ~~~ #


def test_process_instructions():
    m = MemoryV1()
    m.process_instructions(
        ["mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", "mem[8] = 11"]
    )
    assert m.memory[8] == 73


def test_process_instructions_v2():
    m = MemoryV2()
    m.process_instructions(
        [
            "mask = 000000000000000000000000000000X1001X",
            "mem[42] = 100",
            "mask = 00000000000000000000000000000000X0XX",
            "mem[26] = 1",
        ]
    )
    assert m.memory_sum() == 208
