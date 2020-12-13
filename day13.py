#!/usr/bin/env python3

TIMESTAMP = 939


def close_to_ts(bus_id):
    return bus_id - (TIMESTAMP % bus_id)


def closest(buses):
    valid_buses = [int(bus) for bus in buses if bus != "x"]
    return min(valid_buses, key=close_to_ts)


def earliest_sequence(buses):
    ts = 0
    lcm = 1
    bus_tuples = [
        (offset, int(bus_id)) for offset, bus_id in enumerate(buses) if bus_id != "x"
    ]
    for offset, bus_id in bus_tuples:
        while (ts + offset) % bus_id != 0:
            ts += lcm
        lcm *= bus_id
    return ts


def load_input(filename):
    with open(filename) as f:
        return f.readlines()


if __name__ == "__main__":
    data = load_input("day13_input.txt")
    TIMESTAMP = int(data[0])
    buses = data[1].strip().split(",")
    print(f"Part 1: {closest(buses) * close_to_ts(closest(buses))}")
    print(f"Part 2: {earliest_sequence(buses)}")


# ~~~ Tests ~~~ #


def test_closest():
    buses = ["7", "13", "x", "x", "59", "x", "31", "19"]
    assert closest(buses) == 59
    assert closest(buses) * close_to_ts(closest(buses)) == 295


def test_earliest_sequence():
    buses = ["7", "13", "x", "x", "59", "x", "31", "19"]
    assert earliest_sequence(buses) == 1068781
