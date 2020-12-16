#!/usr/bin/env python3


def find_invalid_sum(fields, nearby):
    valid_vals = set().union(*fields.values())
    return sum(val for vals in nearby for val in vals if val not in valid_vals)


def filter_invalid_tickets(fields, nearby):
    valid_vals = set().union(*fields.values())
    valid_tickets = []
    for ticket in nearby:
        if all([val in valid_vals for val in ticket]):
            valid_tickets.append(ticket)
    return valid_tickets


def find_field_positions(fields, valid_tickets):
    field_positions = {}
    for pos in range(len(valid_tickets[0])):
        val_ranges = [ticket[pos] for ticket in valid_tickets]
        for field in fields:
            if all(val in fields[field] for val in val_ranges):
                field_positions.setdefault(field, [])
                field_positions[field].append(pos)
                continue
    determined = {}
    while len(determined) < len(field_positions):
        for field in field_positions:
            if len(field_positions[field]) == 1:
                for other_field in field_positions:
                    if (
                        field != other_field
                        and field_positions[field][0] in field_positions[other_field]
                    ):
                        field_positions[other_field].remove(field_positions[field][0])
                determined[field] = field_positions[field][0]

    return determined


def find_departure_product(field_positions, ticket):
    result = 1
    for field in field_positions:
        if field.startswith("departure"):
            result *= ticket[field_positions[field]]
    return result


def parse_input(lines):
    fields = {}
    yours = []
    nearby = []
    parsing = "fields"
    for line in lines:
        if line == "":
            if parsing == "nearby":
                break
            if parsing == "yours":
                parsing = "nearby"
            if parsing == "fields":
                parsing = "yours"
            continue
        if parsing == "fields":
            field_name, field_values_joint = line.split(": ")
            field_values = field_values_joint.strip().split(" or ")
            fields[field_name] = set()
            for field_value in field_values:
                low, high = field_value.split("-")
                for num in range(int(low), int(high) + 1):
                    fields[field_name].add(num)
        if parsing == "yours":
            if line.strip() == "your ticket:":
                continue
            yours = [int(item) for item in line.strip().split(",")]
        if parsing == "nearby":
            if line.strip() == "nearby tickets:":
                continue
            nearby.append([int(item) for item in line.strip().split(",")])

    return fields, yours, nearby


def load_input(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


if __name__ == "__main__":
    lines = load_input("day16_input.txt")
    fields, yours, nearby = parse_input(lines)
    print(f"Part 1: {find_invalid_sum(fields, nearby)}")
    valid_tickets = filter_invalid_tickets(fields, nearby)
    field_positions = find_field_positions(fields, valid_tickets)
    print(f"Part 2: {find_departure_product(field_positions, yours)}")


# ~~~ Tests ~~~ #


TEST_LINES = [
    "class: 1-3 or 5-7",
    "row: 6-11 or 33-44",
    "seat: 13-40 or 45-50",
    "",
    "your ticket:",
    "7,1,14",
    "",
    "nearby tickets:",
    "7,3,47",
    "40,4,50",
    "55,2,20",
    "38,6,12",
]


def test_parse_input():
    fields, yours, nearby = parse_input(TEST_LINES)
    assert len(fields) == 3
    assert fields["class"] == {1, 2, 3, 5, 6, 7}
    assert yours == [7, 1, 14]
    assert len(nearby) == 4
    assert nearby[0] == [7, 3, 47]


def test_find_invalid_sum():
    fields, _, nearby = parse_input(TEST_LINES)
    assert find_invalid_sum(fields, nearby) == 71


def test_filter_invalid_tickets():
    fields, _, nearby = parse_input(TEST_LINES)
    valid_tickets = filter_invalid_tickets(fields, nearby)
    assert len(valid_tickets) == 1
    assert valid_tickets[0] == [7, 3, 47]
