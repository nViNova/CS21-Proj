from A2 import *


def test_overflowing_with_cf_addc_mba():
    print("running tests for addc-mba")
    REG["ACC"] = "1111"
    MEM[REG["RB"] + REG["RA"]] = "1111"
    REG["CF"] = "1"

    emulate_instruction("addc-mba")

    print(REG["CF"])
    print(REG["ACC"])
    assert REG["CF"] == "1"
    assert REG["ACC"] == "1111"


def test_overflowing_inc_mba():
    print("running tests for inc-mba")

    MEM[REG["RB"] + REG["RA"]] = "0111"
    emulate_instruction("inc*-mba")
    print(MEM[REG["RB"] + REG["RA"]])

    MEM[REG["RB"] + REG["RA"]] = "1111"
    emulate_instruction("inc*-mba")
    print(MEM[REG["RB"] + REG["RA"]])


def test_underflowing_dec_mba():
    print("running tests for dec-mba")

    MEM[REG["RB"] + REG["RA"]] = "0001"
    emulate_instruction("dec*-mba")
    print(MEM[REG["RB"] + REG["RA"]])

    MEM[REG["RB"] + REG["RA"]] = "0000"
    emulate_instruction("dec*-mba")
    print(MEM[REG["RB"] + REG["RA"]])


test_overflowing_with_cf_addc_mba()
test_overflowing_inc_mba()
test_underflowing_dec_mba()
