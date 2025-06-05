import pyxel as px

REG: dict[str, str] = {
    "RA": "0000",  # 4 bits
    "RB": "0000",
    "RD": "0000",
    "RE": "0000",
    "RC": "0000",
    "ACC": "0000",  # 4 bits
    "CF": "0",  # 1 bit
    "TEMP": "0000000000000000",  # 16 bits
}

MEM: dict[str, str] = {
    f"{i:08b}": "0000" for i in range(256)
}  # memory address is 8 bits wide, all memory set to 0 at init

def rotate(register: str, is_right: bool) -> str:
    register_list = list(register)
    if is_right:
        register_list.insert(0, register_list[-1])
        register_list.pop()
        return "".join(register_list)
    else:
        register_list.append(register_list[0])
        register_list.pop(0)
        return "".join(register_list)


def emulate_instruction(instr: str):
    instr_args = instr.split()

    if len(instr_args) == 1:
        instr_only = instr_args[0]

        if instr_only == "rot-r":
            REG["ACC"] = rotate(REG["ACC"], True)

        elif instr_only == "rot-l":
            REG["ACC"] = rotate(REG["ACC"], False)

        elif instr_only == "rot-rc":
            cfAcc = REG["CF"] + REG["ACC"]
            cfAcc = rotate(cfAcc, True)
            REG["CF"] = cfAcc[0]
            REG["ACC"] = cfAcc[1:]

        elif instr_only == "rot-lc":
            cfAcc = REG["CF"] + REG["ACC"]
            cfAcc = rotate(cfAcc, False)
            REG["CF"] = cfAcc[0]
            REG["ACC"] = cfAcc[1:]

        elif instr_only == "from-mba":
            REG["ACC"] = MEM[REG["RB"] + REG["RA"]]

        elif instr_only == "to-mba":
            MEM[REG["RB"] + REG["RA"]] = REG["ACC"]

        elif instr_only == "from-mdc":
            REG["ACC"] = MEM[REG["RD"] + REG["RC"]]

        elif instr_only == "to-mdc":
            MEM[REG["RD"] + REG["RC"]] = REG["ACC"]

        elif instr_only == "addc-mba":
            add_with_carry = (
                int(REG["ACC"], 2)
                + int(MEM[REG["RB"] + REG["RA"]], 2)
                + int(REG["CF"], 2)
            )
            add_with_carry_bit_str = f"{add_with_carry:b}"
            print(add_with_carry_bit_str)
            if len(add_with_carry_bit_str) > 4:
                REG["CF"] = add_with_carry_bit_str[0]
                REG["ACC"] = add_with_carry_bit_str[1:]
            else:
                REG["CF"] = "0"
                REG["ACC"] = add_with_carry_bit_str

        # remove cf from input
        elif instr_only == "add-mba":
            add_with_carry = int(REG["ACC"], 2) + int(MEM[REG["RB"] + REG["RA"]], 2)
            add_with_carry_bit_str = f"{add_with_carry:b}"
            print(add_with_carry_bit_str)
            if len(add_with_carry_bit_str) > 4:
                REG["CF"] = add_with_carry_bit_str[0]
                REG["ACC"] = add_with_carry_bit_str[1:]
            else:
                REG["CF"] = "0"
                REG["ACC"] = add_with_carry_bit_str

        # replace with -
        elif instr_only == "subc-mba":
            add_with_carry = (
                int(REG["ACC"], 2)
                - int(MEM[REG["RB"] + REG["RA"]], 2)
                + int(REG["CF"], 2)
            )
            add_with_carry_bit_str = f"{add_with_carry:b}"
            print(add_with_carry_bit_str)
            if len(add_with_carry_bit_str) > 4:
                REG["CF"] = add_with_carry_bit_str[0]
                REG["ACC"] = add_with_carry_bit_str[1:]
            else:
                REG["CF"] = "0"
                REG["ACC"] = add_with_carry_bit_str

        # combine both
        elif instr_only == "sub-mba":
            add_with_carry = int(REG["ACC"], 2) - int(MEM[REG["RB"] + REG["RA"]], 2)
            add_with_carry_bit_str = f"{add_with_carry:04b}"
            print(add_with_carry_bit_str)
            if len(add_with_carry_bit_str) > 4:
                REG["CF"] = add_with_carry_bit_str[0]
                REG["ACC"] = add_with_carry_bit_str[1:]
            else:
                REG["CF"] = "0"
                REG["ACC"] = add_with_carry_bit_str

        # increase MEM[b:a] by 1
        elif instr_only == "inc*-mba":
            # overflow handling
            new_ba = (int(MEM[REG["RB"] + REG["RA"]], 2) + 1) % 16
            new_ba_string = f"{new_ba:04b}"
            MEM[REG["RB"] + REG["RA"]] = new_ba_string

        # decrease MEM[b:a] by 1
        elif instr_only == "dec*-mba":
            # underflow handling
            new_ba = (int(MEM[REG["RB"] + REG["RA"]], 2) - 1) % 16
            new_ba_string = f"{new_ba:04b}"
            MEM[REG["RB"] + REG["RA"]] = new_ba_string

        # increase MEM[d:c] by 1
        elif instr_only == "inc*-mdc":
            # overflow handling
            new_dc = (int(MEM[REG["RD"] + REG["RC"]], 2) + 1) % 16
            new_dc_string = f"{new_dc:04b}"
            MEM[REG["RB"] + REG["RA"]] = new_dc_string

        # decrease MEM[d:c] by 1
        elif instr_only == "dec*-mdc":
            # underflow handling
            new_dc = (int(MEM[REG["RD"] + REG["RC"]], 2) - 1) % 16
            new_dc_string = f"{new_dc:04b}"
            MEM[REG["RB"] + REG["RA"]] = new_dc_string

        return

    elif len(instr_args) == 2:
        instr_only, reg = instr_args

        # TODO two param instructions

        ...
    elif len(instr_args) == 3:
        ...
    else:
        raise SyntaxError(f"Invalid Instruction '{instr}'")


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
