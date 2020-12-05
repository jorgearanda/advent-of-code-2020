#!/usr/bin/env python3

import string

REQUIRED_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}


class Passport:
    def __init__(self, fields):
        self.fields = {}
        for field in fields:
            key, value = field.split(":")
            self.fields[key] = value

    def valid(self, strict=False):
        if strict:
            return (
                self.has_required_fields()
                and self.valid_byr()
                and self.valid_iyr()
                and self.valid_eyr()
                and self.valid_hgt()
                and self.valid_hcl()
                and self.valid_ecl()
                and self.valid_pid()
            )
        else:
            return self.has_required_fields()

    def has_required_fields(self):
        return len(REQUIRED_FIELDS) == sum(
            [1 for item in REQUIRED_FIELDS if item in self.fields]
        )

    def valid_byr(self):
        return 1920 <= int(self.fields["byr"]) <= 2002

    def valid_iyr(self):
        return 2010 <= int(self.fields["iyr"]) <= 2020

    def valid_eyr(self):
        return 2020 <= int(self.fields["eyr"]) <= 2030

    def valid_hgt(self):
        if self.fields["hgt"][-2:] == "cm":
            return 150 <= int(self.fields["hgt"][:-2]) <= 193
        elif self.fields["hgt"][-2:] == "in":
            return 59 <= int(self.fields["hgt"][:-2]) <= 76
        else:
            return False

    def valid_hcl(self):
        return self.fields["hcl"][0] == "#" and all(
            c in string.hexdigits for c in self.fields["hcl"][1:]
        )

    def valid_ecl(self):
        return self.fields["ecl"] in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}

    def valid_pid(self):
        return len(self.fields["pid"]) == 9 and all(
            c in string.digits for c in self.fields["pid"][1:]
        )


def process_batch(input_batch):
    return [
        line.strip().replace("\n", " ").split() for line in input_batch.split("\n\n")
    ]


def valid_passports_in_batch(input_batch, strict=False):
    passport_lines = process_batch(input_batch)
    passports = [Passport(line) for line in passport_lines]
    return sum(1 for passport in passports if passport.valid(strict))


def load_input(filename):
    with open(filename) as f:
        return f.read()


if __name__ == "__main__":
    input_batch = load_input("day04_input.txt")
    print(f"Part 1: {valid_passports_in_batch(input_batch)}")
    print(f"Part 2: {valid_passports_in_batch(input_batch, strict=True)}")


# ~~~ Tests ~~~ #


def test_valid_passport():
    p = Passport(
        [
            "ecl:gry",
            "pid:860033327",
            "eyr:2020",
            "hcl:#fffffd",
            "byr:1937",
            "iyr:2017",
            "cid:147",
            "hgt:183cm",
        ]
    )
    assert p.valid()


def test_invalid_passport():
    p = Passport(
        [
            "iyr:2013",
            "ecl:amb",
            "cid:350",
            "eyr:2023",
            "pid:028048884",
            "hcl:#cfa07d",
            "byr:1929",
        ]
    )
    assert not p.valid()


TEST_INPUT_BATCH = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""


def test_process_batch():
    ps = process_batch(TEST_INPUT_BATCH)
    assert len(ps) == 4
    assert len(ps[0]) == 8
    assert len(ps[1]) == 7


def test_valid_passports_in_batch():
    assert valid_passports_in_batch(TEST_INPUT_BATCH) == 2


def test_valid_byr():
    p = Passport({})
    p.fields["byr"] = "2002"
    assert p.valid_byr()
    p.fields["byr"] = "2003"
    assert not p.valid_byr()


def test_valid_hgt():
    p = Passport({})
    p.fields["hgt"] = "60in"
    assert p.valid_hgt()
    p.fields["hgt"] = "190cm"
    assert p.valid_hgt()
    p.fields["hgt"] = "190in"
    assert not p.valid_hgt()
    p.fields["hgt"] = "190"
    assert not p.valid_hgt()


def test_valid_hcl():
    p = Passport({})
    p.fields["hcl"] = "#123abc"
    assert p.valid_hcl()
    p.fields["hcl"] = "#123abz"
    assert not p.valid_hcl()
    p.fields["hcl"] = "123abc"
    assert not p.valid_hcl()


def test_valid_ecl():
    p = Passport({})
    p.fields["ecl"] = "brn"
    assert p.valid_ecl()
    p.fields["ecl"] = "wat"
    assert not p.valid_ecl()


def test_valid_pid():
    p = Passport({})
    p.fields["pid"] = "000000001"
    assert p.valid_pid()
    p.fields["pid"] = "0123456789"
    assert not p.valid_pid()


TEST_FOUR_INVALID_BATCH = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""


def test_four_invalid_strict():
    assert valid_passports_in_batch(TEST_FOUR_INVALID_BATCH, strict=True) == 0


TEST_THREE_VALID_BATCH = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022
"""


def test_three_valid_strict():
    assert valid_passports_in_batch(TEST_THREE_VALID_BATCH, strict=True) == 3
