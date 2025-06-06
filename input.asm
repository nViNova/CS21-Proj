# 10 x 10 grid
# 5 registers, 4 bits each, 1 accumulator, 0 - 4
# each inner column is 4 bits, an entire column should be 10 bits, (although the entire column is 20 bits)
# store player pos in reg 1 2

# initialize vars
rcrd 232
acc 5
to-mba
acc 8
to-mdc
rarb 1
acc 11
to-mba # value used to detect underflow for rows
rarb 2
acc 15
to-mba # value used to detect overflow for rows


# listen for inputs
listen: from-ioa # instr 48, all 4 should be in ACC

# up, down, left, right in that order
# use b-bit to determine which input pressed
b-bit 0 up # go up
b-bit 1 down # go down
b-bit 2 listen
b-bit 3 listen

b listen # if no input, jumpt to listen

# update position, X coord in 1, Y coord in 2

# process Y coord

# up
# decrement reg 1 by 1
up: from-mdc# instruction 9 * 16 = 144 Y coord now in acc
to-reg 4 # store current inner column in reg 4
from-reg 2 # get current lower nibble address from reg 2 RC
rarb 0
sub-mba # decrease by 5 to acc store it in cf
to-reg 2 # store new lower nibble back in reg 2
beqz-cf load_mem_y # if cf is 0, no overflow, proceed to loading memory
dec*-reg 3 # decrease higher nibble by 1
set-cf 0 # reset carry flag

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
from-reg 2 # get current lower nibble address from reg 2 RC
rarb 0
add-mba # increase by 5 to acc store it in cf
to-reg 2 # store new lower nibble back in reg 2
beqz-cf load_mem_y # if cf is 0, no overflow, proceed to loading memory
inc*-reg 3 # increase higher nibble by 1
set-cf 0 # reset carry flag

# check whether border
from-reg 3 # get higher nibble
rarb 2
xor-ba
bnez load_mem_y # if not zero, load mem not border
from-reg 2 # get lower nibble
b-bit 2 gameover # 3rd bit lower nibble is 1, out of bounds, over

load_mem_y: from-reg 4 # get inner column from reg 4
to-mdc # store new inner column in memory
b listen # go back to listening for inputs

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

gameover: shutdown