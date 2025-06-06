# 10 x 10 grid
# 5 registers, 4 bits each, 1 accumulator, 0 - 4
# each inner column is 4 bits, an entire column should be 10 bits, (although the entire column is 20 bits)
# store player pos in reg 1 2

# initialize vars
rcrd 192
acc 8
to-mdc

# listen for inputs
from-ioa # instr 64, all 4 should be in ACC

# up, down, left, right in that order
# use b-bit to determine which input pressed
b-bit 0 144 # go up
b-bit 1 down
b-bit 2 left
b-bit 3 right

b 64 # if no input, jumpt to listen

# update position, X coord in 1, Y coord in 2

# process Y coord

# up
# decrement reg 1 by 1
from-reg 2 # instruction 9 * 16 = 144 Y coord now in acc
dec # decrease acc by 1
b 336


# down
from-reg 2 # instruction 12 * 16 = 192 Y coord now in acc
inc # increase acc by 1
b 336

# process X coord

# left
from-reg 1 # instruction X coord now in acc
dec
b 384

# right
from-reg 1 # instruction X coord now in acc
inc
b 384

# process coords Y
bcd # instruction, 21 * 16 = 336 handle overflow
to-reg 2
b updatescreen

# process coords X
bcd # instruction, 24 * 16 = 384 handle overflow
to-reg 1

# updatescreen
# new coord still in acc
# get x, y coords from registers draw them in MEM[RD:RC]

# mul by 5 
# multiply whatever is in acc by 5


# increase column
beqz-cf 80 # when cf is 0, within column, dont increase

inc*-reg 2 # increase column

rot-rc
to-mdc
bnez 80
# increase row
beqz 48