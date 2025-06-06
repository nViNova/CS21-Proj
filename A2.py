import pyxel as px

REG: dict[str, str] = {
    "RA": "0000",  # 4 bits
    "RB": "0000",
    "RC": "0000",
    "RD": "0000",
    "RE": "0000",
    "ACC": "0000",  # 4 bits
    "CF": "0",  # 1 bit
    "TEMP": "0000000000000000",  # 16 bits
    "PC": "0000000000000000",
    "IOA": "0000",  # 4 bits
}

REG_BASE_10_MAPPER: dict[str, str] = {
    "0": "RA",
    "1": "RB",
    "2": "RC",
    "3": "RD",
    "4": "RE",
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

        elif instr_only == "and-ba":
            and_int = int(REG["ACC"], 2) & int(MEM[REG["RB"] + REG["RA"]], 2)
            REG["ACC"] = f"{and_int:04b}"

        elif instr_only == "xor-ba":
            and_int = int(REG["ACC"], 2) ^ int(MEM[REG["RB"] + REG["RA"]], 2)
            REG["ACC"] = f"{and_int:04b}"

        elif instr_only == "or-ba":
            and_int = int(REG["ACC"], 2) | int(MEM[REG["RB"] + REG["RA"]], 2)
            REG["ACC"] = f"{and_int:04b}"

        elif instr_only == "and*-mba":
            and_int = int(REG["ACC"], 2) & int(MEM[REG["RB"] + REG["RA"]], 2)
            MEM[REG["RB"] + REG["RA"]] = f"{and_int:04b}"

        elif instr_only == "xor*-mba":
            and_int = int(REG["ACC"], 2) ^ int(MEM[REG["RB"] + REG["RA"]], 2)
            MEM[REG["RB"] + REG["RA"]] = f"{and_int:04b}"

        elif instr_only == "or*-mba":
            and_int = int(REG["ACC"], 2) | int(MEM[REG["RB"] + REG["RA"]], 2)
            MEM[REG["RB"] + REG["RA"]] = f"{and_int:04b}"

        elif instr_only == "clr-cf":
            REG["CF"] = "0"

        elif instr_only == "set-cf":
            REG["CF"] = "1"

        elif instr_only == "ret":
            pc_as_list = list(REG["PC"])
            temp_as_list = list(REG["TEMP"])
            pc_as_list[4:] = temp_as_list[4:]
            REG["PC"] = "".join(pc_as_list)
            REG["TEMP"] = "0000000000000000"

        elif instr_only == "from-ioa":
            REG["ACC"] = REG["IOA"]

        elif instr_only == "inc":
            acc_int = (int(REG["ACC"], 2) + 1) % 16
            REG["ACC"] = f"{acc_int:04b}"

        elif instr_only == "bcd":
            if int(REG["ACC"], 2) >= 10 or REG["CF"] == 1:
                acc_int = (int(REG["ACC"], 2) + 6) % 16
                REG["ACC"] = f"{acc_int:04b}"
                REG["CF"] = "1"

        elif instr_only == "shutdown":
            exit()

        elif instr_only == "nop":
            ...

        elif instr_only == "dec":
            acc_int = (int(REG["ACC"], 2) - 1) % 16
            REG["ACC"] = f"{acc_int:04b}"

        # TODO commands from 49

    elif len(instr_args) == 2:
        instr_only, reg = instr_args

        if instr_only == "inc*-reg":
            reg_int = (int(REG[REG_BASE_10_MAPPER[reg]], 2) + 1) % 16
            reg_int_str = f"{reg_int:04b}"
            REG[REG_BASE_10_MAPPER[reg]] = reg_int_str

        elif instr_only == "dec*-reg":
            reg_int = (int(REG[REG_BASE_10_MAPPER[reg]], 2) - 1) % 16
            reg_int_str = f"{reg_int:04b}"
            REG[REG_BASE_10_MAPPER[reg]] = reg_int_str

        elif instr_only == "to-reg":
            REG[REG_BASE_10_MAPPER[reg]] = REG["ACC"]

        elif instr_only == "from-reg":
            REG["ACC"] = REG[REG_BASE_10_MAPPER[reg]]

        # The rest of regs from here will be imm values
        # note that reg/imm is in base 10

        elif instr_only == "add":
            if len(f"{reg:04b}") > 4:
                raise ValueError(f"Invalid Immediate Value {reg}")
            acc_int = (
                int(REG["ACC"], 2) + int(reg)
            ) % 16  # convert reg from str to int for ops
            REG["ACC"] = f"{acc_int:04b}"

        elif instr_only == "sub":
            if len(f"{reg:04b}") > 4:
                raise ValueError(f"Invalid Immediate Value {reg}")
            acc_int = (
                int(REG["ACC"], 2) - int(reg)
            ) % 16  # convert reg from str to int for ops
            REG["ACC"] = f"{acc_int:04b}"

        elif instr_only == "and":
            if len(f"{reg:04b}") > 4:
                raise ValueError(f"Invalid Immediate Value {reg}")
            acc_int = int(REG["ACC"], 2) & int(
                reg
            )  # convert reg from str to int for ops
            REG["ACC"] = f"{acc_int:04b}"

        elif instr_only == "xor":
            if len(f"{reg:04b}") > 4:
                raise ValueError(f"Invalid Immediate Value {reg}")
            acc_int = int(REG["ACC"], 2) ^ int(
                reg
            )  # convert reg from str to int for ops
            REG["ACC"] = f"{acc_int:04b}"

        elif instr_only == "or":
            if len(f"{reg:04b}") > 4:
                raise ValueError(f"Invalid Immediate Value {reg}")
            acc_int = int(REG["ACC"], 2) | int(
                reg
            )  # convert reg from str to int for ops
            REG["ACC"] = f"{acc_int:04b}"

        elif instr_only == "r4":
            if len(f"{reg:04b}") > 4:
                raise ValueError(f"Invalid Immediate Value {reg}")
            REG["RE"] = f"{reg:04b}"

        elif instr_only == "rarb":
            if len(f"{reg:08b}") > 8:
                raise ValueError(f"Invalid Immediate Value {reg}")
            imm_str = f"{reg:08b}"
            XXXX, YYYY = imm_str[:4], imm_str[4:]
            REG["RA"] = XXXX
            REG["RB"] = YYYY

        elif instr_only == "rcrb":
            if len(f"{reg:08b}") > 8:
                raise ValueError(f"Invalid Immediate Value {reg}")
            imm_str = f"{reg:08b}"
            XXXX, YYYY = imm_str[:4], imm_str[4:]
            REG["RC"] = XXXX
            REG["RD"] = YYYY

        elif instr_only == "acc":
            if len(f"{int(reg):04b}") > 4:
                raise ValueError(f"Invalid Immediate Value {reg}")
            REG["ACC"] = f"{(int(reg)):04b}"

        # TODO instructions past 67

    elif len(instr_args) == 3:
        ...
    else:
        raise SyntaxError(f"Invalid Instruction '{instr}'")

    # update pc every instruction ran by the instruciton bit width
    pc_update_int = (int(REG["PC"], 2) + 16) % 0b1111_1111_1111_11111
    REG["PC"] = f"{pc_update_int:016b}"


def main_func(commands: list[str]):
    while True:
        curr_PC = int(REG["PC"], 2)
        curr_PC //= 16
        emulate_instruction(commands[curr_PC])
