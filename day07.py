#!/usr/bin/env python3


def parse_rule(rule_text):
    rule_text = rule_text[:-1].replace(" bags", "").replace(" bag", "")
    rules_for, contain_reqs = rule_text.split(" contain ")
    rules = {}
    for rule in contain_reqs.split(", "):
        rule_bits = rule.split(" ")
        if rule_bits[0] != "no":
            rules[" ".join(rule_bits[1:])] = int(rule_bits[0])
    return rules_for, rules


def parse_rules(rules_lines):
    brs = {}
    for line in rules_lines:
        rule_key, rule_val = parse_rule(line.strip())
        brs[rule_key] = rule_val
    return brs


def can_contain_directly(colour, brs):
    return [br for br in brs if colour in brs[br]]


def can_contain(colour, brs):
    can_contain = set()
    bags = can_contain_directly(colour, brs)
    while len(bags) > 0:
        can_contain.add(bags[0])
        bags.extend(can_contain_directly(bags[0], brs))
        bags.pop(0)
    return len(can_contain)


def must_have(colour, brs):
    bag_total = 1
    for br in brs[colour]:
        bag_total += brs[colour][br] * must_have(br, brs)
    return bag_total


def load_input(filename):
    with open(filename) as f:
        return f.readlines()


if __name__ == "__main__":
    bagagge_rules = parse_rules(load_input("day07_input.txt"))
    print(f"Part 1: {can_contain('shiny gold', bagagge_rules)}")
    print(f"Part 2: {must_have('shiny gold', bagagge_rules) - 1}")


# ~~~ Tests ~~~ #


def test_rule_parsing():
    rules_for, rules = parse_rule(
        "light red bags contain 1 bright white bag, 2 muted yellow bags."
    )
    assert rules_for == "light red"
    assert len(rules) == 2
    assert rules["bright white"] == 1
    assert rules["muted yellow"] == 2

    rules_for, rules = parse_rule("bright white bags contain 1 shiny gold bag.")
    assert rules_for == "bright white"
    assert len(rules) == 1
    assert rules["shiny gold"] == 1

    rules_for, rules = parse_rule("faded blue bags contain no other bags.")
    assert rules_for == "faded blue"
    assert len(rules) == 0


TEST_RULES = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""


def test_rules_parsing():
    brs = parse_rules(TEST_RULES.split("\n"))
    assert len(brs) == 9
    assert len(brs["light red"]) == 2
    assert brs["light red"]["bright white"] == 1
    assert brs["light red"]["muted yellow"] == 2


def test_can_contain_shiny_gold():
    brs = parse_rules(TEST_RULES.split("\n"))
    assert can_contain("shiny gold", brs) == 4


def test_shiny_gold_must_have():
    brs = parse_rules(TEST_RULES.split("\n"))
    assert must_have("shiny gold", brs) == 33
