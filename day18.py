#!/usr/bin/env python3

from math import prod
import string


class ExpressionLeftToRight:
    def __init__(self, text):
        while "(" in text or ")" in text:
            last_parens = text.index("(")
            for i in range(last_parens + 1, len(text)):
                if text[i] == "(":
                    last_parens = i
                elif text[i] == ")":
                    text = (
                        text[:last_parens]
                        + str(
                            ExpressionLeftToRight(text[last_parens + 1 : i]).evaluate()
                        )
                        + text[i + 1 :]
                    )
                    break

        self.tokens = []
        for token in text.split(" "):
            if all([char in string.digits for char in token]):
                self.tokens.append(int(token))
            elif token in "+*":
                self.tokens.append(token)
            else:
                print(f"Unexpected token: {token}")

    def evaluate(self):
        result = self.tokens[0]
        operator = "+"
        for token in self.tokens[1:]:
            if isinstance(token, int):
                if operator == "+":
                    result += token
                else:
                    result *= token
            elif token in "+*":
                operator = token
        return result


class ExpressionSumFirst:
    def __init__(self, text):
        while "(" in text or ")" in text:
            last_parens = text.index("(")
            for i in range(last_parens + 1, len(text)):
                if text[i] == "(":
                    last_parens = i
                elif text[i] == ")":
                    text = (
                        text[:last_parens]
                        + str(ExpressionSumFirst(text[last_parens + 1 : i]).evaluate())
                        + text[i + 1 :]
                    )
                    break

        tokens = text.split(" ")
        while "+" in tokens:
            plus_idx = tokens.index("+")
            tokens = (
                tokens[: plus_idx - 1]
                + [str(int(tokens[plus_idx - 1]) + int(tokens[plus_idx + 1]))]
                + tokens[plus_idx + 2 :]
            )

        self.tokens = []
        for token in tokens:
            if all([char in string.digits for char in token]):
                self.tokens.append(int(token))
            elif token == "*":
                self.tokens.append(token)
            else:
                print(f"Unexpected token: {token}")

    def evaluate(self):
        return prod([token for token in self.tokens if isinstance(token, int)])


def load_input(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


if __name__ == "__main__":
    lines = load_input("day18_input.txt")
    print(f"Part 1: {sum([ExpressionLeftToRight(line).evaluate() for line in lines])}")
    print(f"Part 2: {sum([ExpressionSumFirst(line).evaluate() for line in lines])}")


# ~~~ Tests ~~~ #


def test_simple():
    assert ExpressionLeftToRight("3 + 2").evaluate() == 5
    assert ExpressionLeftToRight("3 * 2").evaluate() == 6


def test_left_to_right():
    assert ExpressionLeftToRight("1 + 2 * 3 + 4 * 5 + 6").evaluate() == 71


def test_simple_parens():
    assert ExpressionLeftToRight("2 * 3 + (4 * 5)").evaluate() == 26


def test_complex_parens():
    assert ExpressionLeftToRight("1 + (2 * 3) + (4 * (5 + 6))").evaluate() == 51
    assert (
        ExpressionLeftToRight("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))").evaluate()
        == 12240
    )
    assert (
        ExpressionLeftToRight(
            "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
        ).evaluate()
        == 13632
    )


def test_simple_sum_first():
    assert ExpressionSumFirst("3 + 2").evaluate() == 5
    assert ExpressionSumFirst("3 * 2").evaluate() == 6


def test_sum_first():
    assert ExpressionSumFirst("1 + 2 * 3 + 4 * 5 + 6").evaluate() == 231


def test_sum_first_parens():
    assert ExpressionSumFirst("2 * 3 + (4 * 5)").evaluate() == 46


def test_sum_first_complex_parens():
    assert ExpressionSumFirst("1 + (2 * 3) + (4 * (5 + 6))").evaluate() == 51
    assert (
        ExpressionSumFirst("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))").evaluate()
        == 669060
    )
    assert (
        ExpressionSumFirst("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2").evaluate()
        == 23340
    )
