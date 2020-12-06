#!/usr/bin/env python3


class DeclarationForm:
    def __init__(self, answers):
        self.answers = answers

    def yes_count(self, method="any"):
        if method == "any":
            return len(set(answer for answer in self.answers if answer != " "))
        else:
            family_answers = self.answers.split(" ")
            all_yes = set(family_answers[0])
            for person_answers in family_answers[1:]:
                all_yes = all_yes.intersection(set(person_answers))
            return len(all_yes)


def process_batch(input_batch):
    return [line.strip().replace("\n", " ") for line in input_batch.split("\n\n")]


def yes_count_in_batch(input_batch, method="any"):
    declaration_form_lines = process_batch(input_batch)
    dfs = [DeclarationForm(line) for line in declaration_form_lines]
    return sum(df.yes_count(method=method) for df in dfs)


def load_input(filename):
    with open(filename) as f:
        return f.read()


if __name__ == "__main__":
    input_batch = load_input("day06_input.txt")
    print(f"Part 1: {yes_count_in_batch(input_batch, method='any')}")
    print(f"Part 1: {yes_count_in_batch(input_batch, method='all')}")


# ~~~ Tests ~~~ #


def test_simple():
    df = DeclarationForm("abac")
    assert df.yes_count() == 3


TEST_INPUT_BATCH = """abc

a
b
c

ab
ac

a
a
a
a

b"""


def test_process_batch():
    dfs = process_batch(TEST_INPUT_BATCH)
    assert len(dfs) == 5
    assert len(dfs[0]) == 3


def test_yes_count_in_batch():
    assert yes_count_in_batch(TEST_INPUT_BATCH, method="any") == 11


def test_yes_count_in_batch_intersect():
    assert yes_count_in_batch(TEST_INPUT_BATCH, method="all") == 6
