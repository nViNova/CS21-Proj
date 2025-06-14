import pyxel as px
from A2 import MEM, REG, emulate_instruction
import argparse


WIDTH = 20
HEIGHT = 10
FPS = 2048

parser = argparse.ArgumentParser(
    prog="Arch 242 Emulator", description="Emulates Arch 242 using Pyxel"
)

parser.add_argument("input_asm")

args = parser.parse_args()

if args.input_asm:
    with open(args.input_asm, "r") as f:
        asm_code = f.read()
        print(f"Loaded assembly code from {args.input_asm}")


class App:
    def __init__(self):
        self.grid: list[list[int]] = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.is_halted = False
        if args.input_asm:
            commands = asm_code.strip()
        else:
            commands = ""
            raise RuntimeError(
                "No assembly code provided. Please provide a valid input file."
            )

        # remove comments, and empty lines
        self.commands = [
            command.split("#")[0].strip()
            for command in commands.splitlines()
            if (not command.startswith("#") and command.strip())
        ]
        # change str branch names to instruction numbers * 2
        for i, command in enumerate(self.commands):
            if ":" in command:
                label = command.split(":")[0].strip()
                label_as_instruction = i * 2
                for j in range(len(self.commands)):
                    cmd_args = self.commands[j].split()
                    cmd_args = [
                        str(label_as_instruction) if arg == label else arg
                        for arg in cmd_args
                    ]
                    self.commands[j] = " ".join(cmd_args)

                self.commands[i] = command.split(":")[1].strip()

        self.stepup = False
        self.step_by_step_mode = False

        print(f"Commands: {self.commands}")
        px.init(WIDTH, HEIGHT, title="Arch 242 Monitor", fps=FPS)
        px.run(self.update, self.draw)

    # receives 8 bits address as a str sets grid using lower nibble
    def parse_byte_to_row_col(self, address: str):
        # Address mapping for sanity checks:
        # 187 188 189 190 191 row -1, underflow
        # 192 193 194 185 196 row 0, bit 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
        # 197 to 201 row 1
        # 202 to 206 row 2
        # 207 to 211 row 3
        # 212 to 216 row 4
        # 217 to 221 row 5
        # 222 to 226 row 6
        # 227 to 231 row 7
        # 232 to 236 row 8
        # 237 238 239 240 241 row 9

        if len(address) != 8:
            raise ValueError("Address must be 8 bits long")

        address_int = int(address, 2)

        if address_int < 192 or address_int > 241:
            raise ValueError("Address must be between 192 and 241 inclusive")

        byte = MEM[address]

        # Important: byte is said to be a string of 8 bits, however MEM only has 4 bits,
        # it is now intepreted that we use the entire 'byte'
        lower_nibble = byte

        row = (address_int - 192) // 5
        col = (address_int - 192) % 5

        for i, bit in enumerate(lower_nibble):
            # print(f'{address_int} {row} {col} Setting grid[{row}][{col * len(lower_nibble) + i}] to {bit}')
            self.grid[row][col * len(lower_nibble) + i] = int(bit)

    def update(self):
        list_ioa = list(REG["IOA"])

        if px.btn(px.KEY_O):
            self.stepup = True
        else:
            self.stepup = False

        if px.btn(px.KEY_UP):
            list_ioa[0] = "1"
        else:
            list_ioa[0] = "0"

        if px.btn(px.KEY_DOWN):
            list_ioa[1] = "1"
        else:
            list_ioa[1] = "0"

        if px.btn(px.KEY_LEFT):
            list_ioa[2] = "1"
        else:
            list_ioa[2] = "0"

        if px.btn(px.KEY_RIGHT):
            list_ioa[3] = "1"
        else:
            list_ioa[3] = "0"

        REG["IOA"] = "".join(list_ioa)

        curr_PC = int(REG["PC"], 2)
        curr_PC //= 2

        if (curr_PC < 0 or curr_PC >= len(self.commands)) and not self.is_halted:
            self.is_halted = True
            print("Program counter out of bounds, ignoring further updates.")
        elif self.is_halted:
            ...
        elif self.stepup or not self.step_by_step_mode:
            emulate_instruction(self.commands[curr_PC])
            # with open("A2.log", "a") as log_file:
            #     log_file.write(f"PC: {REG['PC']} | Command: {self.commands[curr_PC]}\n")
            #     log_file.write(f"Updated REG: {REG}\n")

            # Update grid based on memory
            for address in range(192, 242):
                address_str = f"{address:08b}"
                self.parse_byte_to_row_col(address_str)

    def draw(self):
        px.cls(0)
        for i in range(HEIGHT):
            for j in range(WIDTH):
                px.pset(j, i, 7 if self.grid[i][j] == 1 else 0)


App()
