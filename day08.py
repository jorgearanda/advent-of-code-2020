#!/usr/bin/env python3


class Computer:
    def __init__(self, instructions_text):
        self.instructions = [self.parse_instruction(line) for line in instructions_text]

    def parse_instruction(self, instruction_text):
        tokens = instruction_text.split(" ")
        return [tokens[0], int(tokens[1])]

    def run_instruction(self):
        instruction = self.instructions[self.index]
        self.execution_path.append(self.index)
        if instruction[0] == "acc":
            self.acc += instruction[1]
            self.index += 1
        elif instruction[0] == "nop":
            self.index += 1
        else:
            self.index += instruction[1]

    def run_program(self):
        self.index = 0
        self.acc = 0
        self.execution_path = []
        while self.index not in self.execution_path and self.index != len(
            self.instructions
        ):
            self.run_instruction()
        return self.acc

    def fix_program_corruption(self):
        for fix_point in range(len(self.instructions)):
            fix_instruc = self.instructions[fix_point]
            if fix_instruc[0] == "nop":
                fix_instruc[0] = "jmp"
                self.run_program()
                fix_instruc[0] = "nop"
            elif fix_instruc[0] == "jmp":
                fix_instruc[0] = "nop"
                self.run_program()
                fix_instruc[0] = "jmp"
            if self.index == len(self.instructions):
                return self.acc
        else:
            raise Exception("Unfixable :-(")


def load_input(filename):
    with open(filename) as f:
        return f.readlines()


if __name__ == "__main__":
    program = load_input("day08_input.txt")
    computer = Computer(program)
    print(f"Part 1: {computer.run_program()}")
    print(f"Part 2: {computer.fix_program_corruption()}")


# ~~~ Tests ~~~ #


TEST_PROGRAM = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""


def test_program():
    comp = Computer(TEST_PROGRAM.split("\n"))
    assert comp.run_program() == 5


def test_fix_corruption():
    comp = Computer(TEST_PROGRAM.split("\n"))
    assert comp.fix_program_corruption() == 8
