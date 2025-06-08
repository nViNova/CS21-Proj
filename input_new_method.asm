# 10 x 10 grid
# 5 registers, 4 bits each, 1 accumulator, 0 - 4
# each inner column is 4 bits, an entire column should be 10 bits, (although the entire column is 20 bits)
# store player pos in reg 1 2

# initialize vars
call init_vars

# add test rcrd
# rd/Y: 0001 rc/X: 0111
# Y: 1 X: 7
# this should output 198, inner col: 3

rcrd 23

call GET_ADDRESS_AND_INNER_COL
# at this point, RB:RA should have the address, and inner col should be in MEM[1]
rarb 1 # get inner col
from-mba # get inner col from MEM[1]
call ENCODE_INNER_COLUMN
# at this point, acc should have the encoded inner column value
# # inner col now in acc
call DRAW

# 0000 -> 1000 0 = 8
# 0001 -> 0100 1 = 4
# 0010 -> 0010 2 = 2
# 0011 -> 0001 3 = 1

b gameover

ENCODE_INNER_COLUMN: beqz BIT_0 # all 0s, BIT_0
b-bit 3 CHECK_BIT_2 # bit 3 is one, either 1 or 3
b-bit 2 BIT_2 # when above check didnt go, only b2 is one BIT_2
CHECK_BIT_2: b-bit 2 BIT_3 # bit 2 is also one, now a BIT_3
b BIT_1 # above check didnt go # only bit 3 is one, now a BIT_1

BIT_0: acc 8
ret
BIT_1: acc 4
ret
BIT_2: acc 2
ret
BIT_3: acc 1
ret

# Given addressin RD:RC, inner col in ACC

DRAW: to-mdc
ret


# ----------------
# Draw a pixel on the screen given X: RC, Y: RD
# ----------------

# GIVEN
# row = (address_int - 192) // 5
# col = (address_int - 192) % 5
# for i, bit in enumerate(lower_nibble):
#            self.grid[row][col * len(lower_nibble) + i] = int(bit)

# One can get
# 5 * Y + X // 4 + 192 = address_int
# inner_col = X % 4 TODO check later

# =-------=
# Address and Inner Col Getter Func
# Receives X: RC, Y: RD
# Side Effects:
# Modifies RB:RA
# Modifies ACC
# Modifies MEM[RB:RA]
# Modifies CF
# Modifies RD:RC to store TMP values for RB:RA
# Has inner functions prefixed with GA_
# =-------=

# create general get address func
# work with MEM[RB:RA] to store the result
# multiply Y by 5 add X // 4, then add 192 and store it in RB:RA
# X is stored in RC right now.
# Y is stored in RD right now.

GET_ADDRESS_AND_INNER_COL: from-reg 2 # get X from RC

# GET INNER COL

# get its remainder first, for use later
rot-lc
clr-cf
rot-lc
clr-cf
# last 2 bits in LSB now empty, first two bits contains remainder
rot-r
rot-r
# this is the remainder, store it in memory
rarb 1 # set address
to-mba # store remainder in MEM[1]
# now actually divide it
from-reg 2
rot-rc
clr-cf
rot-rc
clr-cf
# acc has the quotient store it in MEM[2]
rarb 2
to-mba
# now we have X // 4 in MEM[2] and the remainder in MEM[1]

# GET ADDRESS
rarb 4 
acc 4
to-mba # init counter var

# now we need to multiply the row by 5
from-reg 3 # Get Y from RD
rarb 0
to-mba # store current acc in temp memory

rcrd 0 # clear these registers for use as TMP RB:RA

# add acc to itself 5 times.

GA_self_add: add-mba # acc = acc + acc
to-reg 2 # store it in RC, lower nibble of address
# check cf
beqz-cf GA_get_next_address
# now cf is 1, increase MSB by 1
inc*-reg 3 # increment RD, upper nibble of address
GA_get_next_address: rarb 3 # tmp mem var
to-mba # store acc in tmp
rarb 4 # get counter var
dec*-mba # decrement counter
from-mba
beqz GA_done
# if not zero, go back to self add
rarb 3
from-mba # restore acc
rarb 0 # restore RB:RA
b GA_self_add

GA_done: rarb 2 # prep RARB for adding X // 4, at this point, RD:RC is the multiplied value
from-reg 2 # get lower nibble of address
add-mba # add X // 4 to the address
to-reg 2 # store it in RC, lower nibble of address
# check for cf
beqz-cf GA_next
# if cf is 1, increment upper nibble of address
inc*-reg 3 # increment RD, upper nibble of address
GA_next: rarb 92 # prep RARB for adding 192
from-reg 3 # get upper nibble of address
add-mba # add 192 to the address
to-reg 3 # store it in RD, upper nibble of address
# now RD:RC has the address, remainder is in MEM[1], and X // 4 is in MEM[2]
ret

# 
# UP 
#

gameover: shutdown

# =------------------------------=
#  FUNCTIONS USED BY THINGS ABOVE
# =------------------------------=

init_vars: rarb 92 # upper nibble of 192
acc 12
to-mba # store upper nibble of 192 in MEM[92]
ret