#!/usr/bin/env python3


class Rule:
    def __init__(self, text):
        if '"' in text:
            self.type = "leaf"
            self.value = text[1]
        elif "|" in text:
            self.type = "or"
            self.alts = [Rule(branch) for branch in text.split(" | ")]
        else:
            self.type = "sequence"
            self.sequence = [int(x) for x in text.split()]

    def is_leaf_valid(self, text):
        if len(text) == 0:
            return False, [""]
        if text[0] == self.value:
            return True, [text[1:]]
        else:
            return False, [""]

    def is_sequence_valid(self, text, rules):
        texts = [text]
        for rule in self.sequence:
            valid_remainders = []
            for text in texts:
                valid, remainders = rules[rule].matches(text, rules)
                if valid:
                    valid_remainders += remainders
            if len(valid_remainders) == 0:
                return False, ""
            texts = valid_remainders
        return True, texts

    def is_option_valid(self, text, rules):
        remainders = []
        for branch in self.alts:
            valid, remainder = branch.matches(text, rules)
            if valid:
                remainders += remainder
        if len(remainders) == 0:
            return False, ""
        return True, remainders

    def matches(self, text, rules):
        if self.type == "leaf":
            return self.is_leaf_valid(text)
        elif self.type == "sequence":
            return self.is_sequence_valid(text, rules)
        else:
            return self.is_option_valid(text, rules)

    def is_valid(self, text, rules):
        result = self.matches(text, rules)
        return result[0] and (len(result[1]) == 0 or len(result[1][0]) == 0)


def load_input(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


if __name__ == "__main__":
    lines = load_input("day19_input.txt")
    rules = {}
    samples = []
    parsing_rules = True
    for line in lines:
        if line == "":
            parsing_rules = False
            continue
        if parsing_rules:
            rule_id, rule_text = line.split(": ")
            rules[int(rule_id)] = Rule(rule_text)
        else:
            samples.append(line)
    matching_messages = sum(
        [1 for sample in samples if rules[0].is_valid(sample, rules)]
    )
    print(f"Part 1: {matching_messages}")
    rules[8] = Rule("42 | 42 8")
    rules[11] = Rule("42 31 | 42 11 31")
    matching_messages = sum(
        [1 for sample in samples if rules[0].is_valid(sample, rules)]
    )
    print(f"Part 2: {matching_messages}")


# ~~~ Tests ~~~ #


def test_only_leaf():
    rules = {0: Rule('"a"')}
    assert rules[0].is_valid("a", rules) == True
    assert rules[0].is_valid("b", rules) == False


def test_single_branch():
    rules = {0: Rule("1 1 1"), 1: Rule('"a"')}
    assert rules[0].is_valid("aaa", rules) == True
    assert rules[0].is_valid("aa", rules) == False
    assert rules[0].is_valid("aaaa", rules) == False
    assert rules[0].is_valid("aba", rules) == False


def test_first_example():
    rules = {
        0: Rule("1 2"),
        1: Rule('"a"'),
        2: Rule("1 3 | 3 1"),
        3: Rule('"b"'),
    }
    assert rules[0].is_valid("aab", rules) == True
    assert rules[0].is_valid("aba", rules) == True
    assert rules[0].is_valid("bab", rules) == False
    assert rules[0].is_valid("aabb", rules) == False


def test_second_example():
    rules = {
        0: Rule("4 1 5"),
        1: Rule("2 3 | 3 2"),
        2: Rule("4 4 | 5 5"),
        3: Rule("4 5 | 5 4"),
        4: Rule('"a"'),
        5: Rule('"b"'),
    }
    assert rules[0].is_valid("aaaabb", rules) == True
    assert rules[0].is_valid("abbabb", rules) == True
    assert rules[0].is_valid("ababbb", rules) == True
    assert rules[0].is_valid("ababbb", rules) == True
    assert rules[0].is_valid("bababa", rules) == False
    assert rules[0].is_valid("aaabbb", rules) == False


def test_fixture_with_rule_change():
    lines = load_input("day19_fixture.txt")
    rules = {}
    samples = []
    parsing_rules = True
    for line in lines:
        if line == "":
            parsing_rules = False
            continue
        if parsing_rules:
            rule_id, rule_text = line.split(": ")
            rules[int(rule_id)] = Rule(rule_text)
        else:
            samples.append(line)
    matching_messages = sum(
        [1 for sample in samples if rules[0].is_valid(sample, rules)]
    )
    assert matching_messages == 3

    rules[8] = Rule("42 | 42 8")
    rules[11] = Rule("42 31 | 42 11 31")
    matching_messages = sum(
        [1 for sample in samples if rules[0].is_valid(sample, rules)]
    )
    assert matching_messages == 12
