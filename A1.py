import argparse

REG: dict[str, str] = {
    "RA": "000",  # 4 bits
    "RB": "001",
    "RC": "010",
    "RD": "011",
    "RE": "100",
}

NO_REGISTER_INST = {
    "rot-r",
    "rot-l",
    "rot-rc",
    "rot-lc",
    "from-mba",
    "to-mba",
    "from-mdc",
    "to-mdc",
    "addc-mba",
    "add-mba",
    "subc-mba",
    "sub-mba",
    "inc*-mba",
    "dec*-mba",
    "inc*-mdc",
    "dec*-mdc",
}
START_END_INST = {"inc*-reg", "dec*-reg", "to-reg", "from-reg"}
REG_ACC = {"to-reg", "from-reg"}
TRIPLE_INPUT = {"b-bit"}
FOUR_BIT_IMM_SIXTEEN = {"add", "sub", "and", "xor", "or", "r4"}
FOUR_BIT_IMM_EIGHT = {"acc"}
EIGHT_BIT_IMM_SIXTEEN = {"rarb", "rcrd"}
ELEVEN_BIT_IMM_SIXTEEN = {
    "bnz-a",
    "bnz-b",
    "beqz",
    "bnez",
    "beqz-cf",
    "bnez-cf",
    "bnz-d",
}
TWELVE_BIT_IMM_SIXTEEN = {"b", "call"}

INST = {
    "rot-r": "0x00",
    "rot-l": "0x01",
    "rot-rc": "0x02",
    "rot-lc": "0x03",
    "from-mba": "0x04",
    "to-mba": "0x05",
    "from-mdc": "0x06",
    "to-mdc": "0x07",
    "addc-mba": "0x08",
    "add-mba": "0x09",
    "subc-mba": "0x0A",
    "sub-mba": "0x0B",
    "inc*-mba": "0x0C",
    "dec*-mba": "0x0D",
    "inc*-mdc": "0x0E",
    "dec*-mdc": "0x0F",
    "inc*-reg": ("0x1", "0"),
    "dec*-reg": ("0x1", "1"),
    "and-ba": "0x1A",
    "xor-ba": "0x1B",
    "or-ba": "0x1C",
    "and*-mba": "0x1D",
    "xor*-mba": "0x1E",
    "or*-mba": "0x1F",
    "to-reg": ("0x2", "0"),
    "from-reg": ("0x2", "1"),
    "clr-cf": "0x2A",
    "set-cf": "0x2B",
    "ret": "0x2E",
    "from-ioa": "0x32",
    "inc": "0x31",
    "bcd": "0x36",
    "shutdown": "0x373E",
    "nop": "0x3E",
    "dec": "0x3F",
    "add": "0x40",
    "sub": "0x41",
    "and": "0x42",
    "xor": "0x43",
    "or": "0x44",
    "r4": "0x46",
    "rarb": ("0101", "0000"),
    "rcrd": ("0110", "0000"),
    "acc": "0x70",
    "b-bit": "100",
    "bnz-a": "10100",
    "bnz-b": "10101",
    "beqz": "10110",
    "bnez": "10111",
    "beqz-cf": "11000",
    "bnez-cf": "11001",
    "bnz-d": "11011",
    "b": "1110",
    "call": "1111",
}

parser = argparse.ArgumentParser(
    prog="Arch 242 Assembler", description="Converts instructions to machine language"
)

parser.add_argument("input_asm")

parser.add_argument("type")

args = parser.parse_args()

if args.input_asm:
    with open(args.input_asm, "r") as f:
        asm_code = f.read()
        print(f"Loaded assembly code from {args.input_asm}")

if args.input_asm:
    commands = asm_code.strip()
else:
    commands = ""
    raise RuntimeError("No assembly code provided. Please provide a valid input file.")

# remove comments, and empty lines
commands = [
    command.split("#")[0].strip()
    for command in commands.splitlines()
    if (not command.startswith("#") and command.strip())
]
print(f"Commands: {commands}")


def assembler(
    instr: str, form: str
) -> str:  # has to be a str, need to sometimes prepend 0s to hex or bin
    converted_instr = None
    instr: list[str] = instr.split()
    print("converting", instr)

    # Handle .byte directive
    if instr[0].startswith(".byte"):
        val = int(instr.split()[1].lower().replace("0x", ""), 16)
        if form == "bin":
            return f"{val:08b}"
        else:
            return f"{val:08x}"

    # this part all good
    if len(instr) == 1:
        if instr[0] not in INST:
            raise SyntaxError("Invalid Instruction")

        converted_instr = int(
            INST[instr[0]], 16
        )  # turn str to hex to convert properly to bin later
        if form == "bin":
            return f"{converted_instr:016b}"
        return f"{converted_instr:04x}"

    elif len(instr) == 2:
        if instr[0] not in INST:
            raise SyntaxError("Invalid Instruction")

        inst, reg = instr
        if inst in START_END_INST:
            start, end = INST[inst]
            # we are ensured start is at most 4 bits # reg will be a bit string, convert start and end to bit strings as well
            converted_instr = (
                f"{int(start, 16):04b}" + REG[reg] + end
            )  # end is only 1 bit can put it as is

            if form == "bin":
                return "0" * 8 + converted_instr

            # convert to hex
            converted_instr = int(converted_instr, 2)
            return f"{converted_instr:04x}"

        elif inst in FOUR_BIT_IMM_SIXTEEN:
            inst, imm = instr

            # imm will be a base 10 integer
            imm = int(imm)
            hex_imm = f"{imm:01x}"

            if len(hex_imm) > 1:
                raise ValueError("Invalid Immediate, Must be at most 4 bits")

            # combine inst in hex with imm in hex
            converted_instr = INST[inst] + hex_imm

            if form == "hex":
                return (
                    "0" + converted_instr[2:]
                )  # remove 0x and append a 0 at the start

            else:
                converted_instr = int(converted_instr, 16)
                return f"{converted_instr:016b}"

        elif inst in FOUR_BIT_IMM_EIGHT:
            inst, imm = instr
            # imm will be a base 10 integer
            imm = int(imm)

            # convert the values to hex
            hex_inst = int(INST[inst], 16)
            hex_imm = int(hex(int(imm)), 16)

            # Solve the converted instruction in base 10
            converted_instr = hex_inst + hex_imm
            if form == "hex":
                return f"{converted_instr:04x}"  # convert to hex
            else:
                return f"{converted_instr:016b}"  # convert to bin

        elif inst in EIGHT_BIT_IMM_SIXTEEN:
            inst, imm = instr
            imm = int(imm)
            imm_extended = f"{imm:08b}"
            imm_Y = imm_extended[:4]
            imm_X = imm_extended[4:]

            converted_instr = INST[inst][0] + imm_X + INST[inst][1] + imm_Y

            if form == "bin":
                return converted_instr
            else:
                converted_instr = int(converted_instr, 2)
                return f"{converted_instr:04x}"

        elif inst in ELEVEN_BIT_IMM_SIXTEEN:
            inst, imm = instr
            imm = int(imm)
            imm_extended = f"{imm:011b}"
            imm_B = imm_extended[:3]
            imm_A = imm_extended[3:]

            converted_instr = INST[inst] + imm_B + imm_A

            if form == "bin":
                return converted_instr
            else:
                converted_instr = int(converted_instr, 2)
                return f"{converted_instr:04x}"

        elif inst in TWELVE_BIT_IMM_SIXTEEN:
            inst, imm = instr
            imm = int(imm)
            imm_extended = f"{imm:012b}"
            imm_B = imm_extended[:4]
            imm_A = imm_extended[4:]

            converted_instr = INST[inst] + imm_B + imm_A

            if form == "bin":
                return converted_instr
            else:
                converted_instr = int(converted_instr, 2)
                return f"{converted_instr:04x}"

    elif len(instr) == 3:
        inst, k, imm = instr
        k, imm = int(k), int(imm)

        if inst not in TRIPLE_INPUT:
            raise SyntaxError("Invalid Instruction")

        imm_extended = f"{imm:011b}"
        imm_B = imm_extended[:3]
        imm_A = imm_extended[3:]
        converted_instr = INST[inst] + f"{k:02b}" + imm_B + imm_A

        if form == "bin":
            return converted_instr
        else:
            converted_instr = int(converted_instr, 2)
            return f"{converted_instr:04x}"

    else:
        raise SyntaxError("Invalid Instruction")

with open("output.txt", "w") as f:
    for command in commands:
        output = assembler(command, args.type)
        f.write(output + "\n")
