#!/usr/bin/env python3


def prepare_adapters(adapters):
    adapters.append(max(adapters) + 3)  # To account for the device
    return sorted(adapters)


def find_1jolt_3jolt_diffs(adapters):
    diffs = {}
    jolts = 0
    for adapter in adapters:
        diffs.setdefault(adapter - jolts, 0)
        diffs[adapter - jolts] += 1
        jolts = adapter
    return diffs[1] * diffs[3]


def find_arrangements(adapters):
    seq_sizes = {}
    last_jolt = 0
    cur_size = 1
    for adapter in adapters:
        if adapter == last_jolt + 1:
            cur_size += 1
        else:
            seq_sizes.setdefault(cur_size, 0)
            seq_sizes[cur_size] += 1
            cur_size = 1
        last_jolt = adapter
    seq_sizes.setdefault(cur_size, 0)
    seq_sizes[cur_size] += 1

    return (
        2 ** seq_sizes.get(3, 1) * 4 ** seq_sizes.get(4, 1) * 7 ** seq_sizes.get(5, 1)
    )


def load_input(filename):
    with open(filename) as f:
        return [int(line) for line in f.readlines()]


if __name__ == "__main__":
    adapters = prepare_adapters(load_input("day10_input.txt"))
    print(f"Part 1: {find_1jolt_3jolt_diffs(adapters)}")
    print(f"Part 2: {find_arrangements(adapters)}")


# ~~~ Tests ~~~ #


def test_find_1jolt_3jolt_diffs():
    TEST_ADAPTERS = [
        28,
        33,
        18,
        42,
        31,
        14,
        46,
        20,
        48,
        47,
        24,
        23,
        49,
        45,
        19,
        38,
        39,
        11,
        1,
        32,
        25,
        35,
        8,
        17,
        7,
        9,
        4,
        2,
        34,
        10,
        3,
    ]
    assert find_1jolt_3jolt_diffs(prepare_adapters(TEST_ADAPTERS)) == 220


def test_find_arrangements():
    TEST_ADAPTERS = [
        28,
        33,
        18,
        42,
        31,
        14,
        46,
        20,
        48,
        47,
        24,
        23,
        49,
        45,
        19,
        38,
        39,
        11,
        1,
        32,
        25,
        35,
        8,
        17,
        7,
        9,
        4,
        2,
        34,
        10,
        3,
    ]
    assert find_arrangements(prepare_adapters(TEST_ADAPTERS)) == 19208
