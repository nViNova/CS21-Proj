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

rarb 90 # store X value init
acc 3
to-mba # store X value in MEM[90]
rarb 91 # store Y value init
acc 3
to-mba # store Y value in MEM[91]
rarb 100
acc 2
to-mba # store tail score in MEM[100]

# 0000 -> 1000 0 = 8
# 0001 -> 0100 1 = 4
# 0010 -> 0010 2 = 2
# 0011 -> 0001 3 = 1


# All commands associated with drawing a pixel
# At Y: RD, X: RC

start: call LISTEN_INPUT

# store Y: RD, X: RC in tmp memory
rarb 104
from-reg 3 # get Y from RD
to-mba # store Y in MEM[110]
rarb 105
from-reg 2 # get X from RC
to-mba # store X in MEM[111]
# now RD:RC has the new coordinates of the player

# compare X and Y to all tails check for XOR is 0
rarb 100
from-mba # get tail score from MEM[100]
to-reg 4 # store tail score in R4

CHECK_TAIL_LOOP: call get_tail_memory
# at this point, RD:RC has the tail coordinates
rarb 104
from-reg 3 # get Y of tail from RD
xor-ba # XOR with current Y
beqz COMPARE_X # if Y is equal, go to X compare
b CHECK_OTHER_TAILS
COMPARE_X: rarb 105
from-reg 2 # get X of tail from RC
xor-ba # XOR with current X
beqz gameover # if X is equal, die
CHECK_OTHER_TAILS: dec*-reg 4 # decrement tail number
from-reg 4 # get tail number from R4
bnez CHECK_TAIL_LOOP # if tail number is not zero, loop again

# no tails intersect
ALL_GOOD_WITH_TAIL: rarb 104 
from-mba # get Y from MEM[110]
to-reg 3 # store Y in RD
rarb 105
from-mba # get X from MEM[111]
to-reg 2 # store X in RC
# now RD:RC has the coordinates of the player
call GET_ADDRESS_AND_INNER_COL
# at this point, RB:RA should have the address, and inner col should be in ACC
call ENCODE_INNER_COLUMN
# Draw the pixel
to-reg 4 # store inner col in R4
from-reg 3 # get upper nibble
to-reg 1 # store in RB
from-reg 2 # get lower nibble
to-reg 0 # store in RA
# now RB:RA has the address, inner col in R4
from-reg 4 # get inner col from R4
or*-mba # add the pixel to the screen while ignoring already lit pixels

# get stored score
rarb 100 # get tail score from memory
from-mba # get tail score from memory
to-reg 4

# restore X and Y from tmp memory
rarb 104 # get Y from MEM[110]
from-mba # get Y value
to-reg 3 # store Y in RD
rarb 105 # get X from MEM[111]
from-mba # get X value
to-reg 2 # store X in RC

UPDATE_PLAYER_TAILS: from-reg 4 # get snake tail number
rarb 100 # store tail score in memory
to-mba # store tail score in MEM[100]

# store tail coords, current = x, y
rarb 98 # TMP var to store new pos Y of player
from-reg 3 # get Y from RD
to-mba # store Y in TMP var
rarb 99 # TMP var to store new pos X of player
from-reg 2 # get X from RC
to-mba # store X in TMP var

TAILS_LOOP: call get_tail_memory

# at this point, RD:RC has the tail coordinates
# store this at temp vars, prev = x, y
rarb 101 # TMP var to store tail Y
from-reg 3 # get Y from RD
to-mba # store tail Y in TMP var
rarb 102 # TMP var to store tail X
from-reg 2 # get X from RC
to-mba # store tail X in TMP var

# now get the current tail coords x, y = curr
rarb 98 # get new pos Y of player
from-mba # get Y from TMP var
to-reg 3 # store Y in RD
rarb 99 # get new pos X of player
from-mba # get X from TMP var
to-reg 2 # store X in RC
# now RD:RC has the new coordinates of the player

call set_tail_memory

# curr = prev

rarb 101 # get tail Y from TMP var
from-mba # get tail Y from TMP var
to-reg 3 # store tail Y in RD
rarb 102 # get tail X from TMP var
from-mba # get tail X from TMP var
to-reg 2 # store tail X in RC

rarb 98
from-reg 3
to-mba # store new pos Y in MEM[98]
rarb 99
from-reg 2
to-mba # store new pos X in MEM[99]

from-reg 4
beqz LOOP_TAILS_NEAR_DONE

dec*-reg 4 # decrement tail number
b TAILS_LOOP # if not zero, loop again
LOOP_TAILS_NEAR_DONE: call GET_ADDRESS_AND_INNER_COL
# at this point, RB:RA should have the address, and inner col should be in ACC
call ENCODE_INNER_COLUMN
# change the inner column to draw to become a delete
# XOR ur current inner column with 1111 to become its inverse
rarb 103 # TMP var to store inner col
to-mba # store inner col in TMP var
acc 15 # 1111
xor-ba # acc now has the inverse of inner column
# now mask this with the value in mdc
to-reg 4 # store inverse in r4
from-mdc # get current pixel value from mdc
to-mba # store inner col in TMP var
# the tmp var has the current inner column
from-reg 4 # get inverse inner column from R4
and-ba # mask the current pixel value with the inverse inner column
# now whatever pixel needed to be deleted is gone.
call DRAW # this deletes the needed pixel
# pixel deleted, tail memory updated

#
# SPAWN FOOD HERE
#



b start

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

DRAW: to-mdc # tmp fix
ret

LISTEN_INPUT: from-ioa

beqz LISTEN_AGAIN
rarb 106
to-mba # store last known player input in MEM[106]

# up, down, left, right in that order
# use b-bit to determine which input pressed
LISTEN_AGAIN: b-bit 0 INPUT_UP # go up
b-bit 1 INPUT_DOWN # go down
b-bit 2 INPUT_LEFT
b-bit 3 INPUT_RIGHT

rarb 106
from-mba
bnez LISTEN_AGAIN

b LISTEN_INPUT # if no input, jumpt to listen

INPUT_UP: rarb 91 # get Y from MEM[91]
from-mba # get Y value
dec
b PROCESS_INPUT # process input

INPUT_DOWN: rarb 91 # get Y from MEM[91]
from-mba # get Y value
inc
b PROCESS_INPUT # process input

INPUT_LEFT: rarb 90 # get X from MEM[90]
from-mba # get X value
dec
b PROCESS_INPUT

INPUT_RIGHT: rarb 90 # get X from MEM[90]
from-mba # get X value
inc
b PROCESS_INPUT # process input

PROCESS_INPUT: bcd
beqz-cf INPUT_DONE
b gameover # if X is 0 or >10, game over
INPUT_DONE: to-mba # store new whatever coord
rarb 90 # get X from MEM[90]
from-mba # get X value
to-reg 2 # store X in RC
rarb 91 # get Y from MEM[91]
from-mba # get Y value
to-reg 3 # store Y in RD
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
rarb 94 # set address
to-mba # store remainder in MEM[94]
# now actually divide it
from-reg 2
rot-rc
clr-cf
rot-rc
clr-cf
# acc has the quotient store it in MEM[2]
rarb 95
to-mba
# now we have X // 4 in MEM[2] and the remainder in MEM[1]

# GET ADDRESS
rarb 97
acc 4
to-mba # init counter var

# now we need to multiply the row by 5
from-reg 3 # Get Y from RD
rarb 93
to-mba # store current acc in temp memory

rcrd 0 # clear these registers for use as TMP RB:RA

# add acc to itself 5 times.

GA_self_add: add-mba # acc = acc + acc
to-reg 2 # store it in RC, lower nibble of address
# check cf
beqz-cf GA_get_next_address
# now cf is 1, increase MSB by 1
inc*-reg 3 # increment RD, upper nibble of address
GA_get_next_address: rarb 96 # tmp mem var
to-mba # store acc in tmp
rarb 97 # get counter var
dec*-mba # decrement counter
from-mba
beqz GA_done
# if not zero, go back to self add
rarb 96
from-mba # restore acc
rarb 93 # restore RB:RA
b GA_self_add

GA_done: rarb 95 # prep RARB for adding X // 4, at this point, RD:RC is the multiplied value
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
rarb 94 # get inner col
from-mba # get inner col from MEM[1]
# inner col remainder now in ACC
ret

set_tail_memory: from-reg 4 # get snake tail number
rarb 0 # prepare RARB for storing tail memory

#
# Store Y Value  
#

to-reg 0 # store it to RA
from-reg 3 # get Y from RD
to-mba # add Y to RB:RA

#
# Store X Value
#

inc*-reg 1 # increment RB, upper nibble of address
from-reg 2 # get X from RC
to-mba # add X to RB:RA
ret


get_tail_memory: from-reg 4 # get snake tail number
rarb 0 # prepare RARB for getting tail memory

#
# Get Y Value
#

to-reg 0 # store it to RA
from-mba # get Y from RB:RA
to-reg 3 # store Y in RD

#
# Get X Value
#

inc*-reg 1 # increment RB, upper nibble of address
from-mba # get X from RB:RA
to-reg 2 # store X in RC
# now RD:RC has the tail coordinates
ret


gameover: shutdown

# =------------------------------=
#  FUNCTIONS USED BY THINGS ABOVE
# =------------------------------=

init_vars: rarb 92 # upper nibble of 192
acc 12
to-mba # store upper nibble of 192 in MEM[92]
ret