# 10 x 10 grid
# 5 registers, 4 bits each, 1 accumulator, 0 - 4
# each inner column is 4 bits, an entire column should be 10 bits, (although the entire column is 20 bits)
# store player pos in reg 1 2

# initialize vars
rcrd 192 # starting address pos
acc 5
to-mba
acc 8 # starting inner column pos
to-mdc
rarb 1
acc 11
to-mba # value used to detect underflow for rows
rarb 2
acc 15
to-mba # value used to detect overflow for rows
rarb 3
acc 1
to-mba # hack to have carry flags for dec and inc


# listen for inputs
listen: from-ioa # all 4 should be in ACC

# up, down, left, right in that order
# use b-bit to determine which input pressed
b-bit 0 up # go up
b-bit 1 down # go down
b-bit 2 left
b-bit 3 right

b listen # if no input, jumpt to listen

# update position, X coord in 1, Y coord in 2

# process Y coord

# up
# decrement reg 1 by 1
up: from-mdc# instruction 9 * 16 = 144 Y coord now in acc
to-reg 4 # store current inner column in reg 4

# TODO modify this later to support for longer snek
acc 0 # now safe to set acc to 0, old pixel stored
to-mdc # remove old pixel

from-reg 2 # get current lower nibble address from reg 2 RC
rarb 0
sub-mba # decrease by 5 to acc store it in cf
to-reg 2 # store new lower nibble back in reg 2
beqz-cf load_mem_y # if cf is 0, no overflow, proceed to loading memory
dec*-reg 3 # decrease higher nibble by 1
clr-cf # reset carry flag

# check whether border
from-reg 3 # get higher nibble
rarb 1
xor-ba 
beqz gameover # hit border, gameover
b load_mem_y

# down
# change row by 1

# get current row from rd rc
down: from-mdc # get current inner column from memory
to-reg 4 # store current inner column in reg 4

# TODO modify this later to support for longer snek
acc 0 # now safe to set acc to 0, old pixel stored
to-mdc # remove old pixel

from-reg 2 # get current lower nibble address from reg 2 RC
rarb 0
add-mba # increase by 5 to acc store it in cf
to-reg 2 # store new lower nibble back in reg 2
beqz-cf load_mem_y # if cf is 0, no overflow, proceed to loading memory
inc*-reg 3 # increase higher nibble by 1
clr-cf # reset carry flag

# check whether border
from-reg 3 # get higher nibble
rarb 2
xor-ba
bnez load_mem_y # if not zero, load mem not border
from-reg 2 # get lower nibble
b-bit 2 gameover # 3rd bit lower nibble is 1, out of bounds, over


# Process X coord

left: from-mdc # get current inner column from memory
rot-lc # rotate left save overflow to cf
beqz-cf load_mem # no overflow, cf 0, go to load mem

# TODO add border checks here for left

# has overflow go to next inner column
decrease_bit: acc 0
to-mdc # remove old pixel
clr-cf # reset carry flag
rarb 3
from-reg 2 # get current lower nibble address from reg 2 RC
sub-mba # decrease by 1
to-reg 2 # store new lower nibble back in reg 2
acc 1 # set the upcoming acc for the new inner column
beqz-cf load_mem # if not zero, go to load mem
dec*-reg 3 # decrease higher nibble by 1
clr-cf # reset carry flag
b load_mem

right: from-mdc # get current inner column from memory
rot-rc # rotate left save overflow to cf
beqz-cf load_mem # no overflow, cf 0, go to load mem

# TODO add border checks here for right

# has overflow go to next inner column
decrease_bit: acc 0
to-mdc # remove old pixel
clr-cf # reset carry flag
rarb 3

from-reg 2 # get current lower nibble address from reg 2 RC
add-mba # increase by 1
to-reg 2 # store new lower nibble back in reg 2

acc 8 # set the upcoming acc for the new inner column
beqz-cf load_mem # if not zero, go to load mem
inc*-reg 3 # increase higher nibble by 1
clr-cf # reset carry flag
b load_mem # go to load mem

load_mem_y: from-reg 4 # get current inner column from reg 4
load_mem: to-mdc
b listen # go back to listening for inputs


gameover: shutdown