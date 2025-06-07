# 10 x 10 grid
# 5 registers, 4 bits each, 1 accumulator, 0 - 4
# each inner column is 4 bits, an entire column should be 10 bits, (although the entire column is 20 bits)
# store player pos in reg 1 2

# initialize vars
call init_vars

# listen for inputs
listen: from-ioa # all 4 should be in ACC

# up, down, left, right in that order
# use b-bit to determine which input pressed
b-bit 0 up # go up
b-bit 1 down # go down
b-bit 2 left
b-bit 3 right
b listen # if no input, jumpt to listen

# ----------------
# The following code gets address from RD:RC and updates the pixel on 
# the inner column of MEM[RD:RC] at there depending on the called branch
# ----------------

# -----------------
# What does this mean? You can put any arbitrary value in RD:RC and it will update the pixel, 
# meaning you can use this to update the position of any pixel on the screen, even when its not the player.
# -----------------

# ----------------
# process Y coord
# ----------------

# 
# UP 
#

up: call y_init_common # up and down have common instructions, made them into one call

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

#
# DOWN
#

# get current row from rd rc
down: call y_init_common # down and up have common instructions, made them into one call

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

#
# LEFT
#

left: from-mdc # get current inner column from memory
rot-lc # rotate left save overflow to cf
beqz-cf load_mem # no overflow, cf 0, go to load mem

# TODO add border checks here for left

# has overflow go to next inner column
call x_decrease_bit_common # right and left have common instructions, made them into one call
sub-mba # decrease by 1
to-reg 2 # store new lower nibble back in reg 2

acc 1 # set the upcoming acc for the new inner column
beqz-cf load_mem # if not zero, go to load mem
dec*-reg 3 # decrease higher nibble by 1
clr-cf # reset carry flag
b load_mem

#
# RIGHT
#

right: from-mdc # get current inner column from memory
rot-rc # rotate left save overflow to cf
beqz-cf load_mem # no overflow, cf 0, go to load mem

# TODO add border checks here for right

# has overflow go to next inner column
call x_decrease_bit_common # right and left have common instructions, made them into one call

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

# =------------------------------=
#  FUNCTIONS USED BY THINGS ABOVE
# =------------------------------=

init_vars: rcrd 192 # starting address pos
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
ret

y_init_common: from-mdc # get current inner column from memory
to-reg 4 # store current inner column in reg 4

# TODO modify this later to support for longer snek
acc 0 # now safe to set acc to 0, old pixel stored
to-mdc # remove old pixel

from-reg 2 # get current lower nibble address from reg 2 RC
rarb 0
ret

x_decrease_bit_common: acc 0
to-mdc # remove old pixel
clr-cf # reset carry flag
rarb 3
from-reg 2 # get current lower nibble address from reg 2 RC
ret