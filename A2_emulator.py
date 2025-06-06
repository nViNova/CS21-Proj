import pyxel as px
from A2 import *


class App:
    def __init__(self):
        px.init(160, 120)
        self.x = 0
        px.run(self.update, self.draw)

    def update(self):
        command = input()
        emulate_instruction(command)

    def draw(self):
        px.cls(0)
        for reg_i, reg_key in enumerate(REG):
            px.text(0, reg_i * 10, f"{reg_key}: {REG[reg_key]}", 7)
        # px.rect(self.x, 0, 8, 8, 9)


App()
