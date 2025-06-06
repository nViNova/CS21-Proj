# 10 x 10 grid
# 5 registers, 4 bits each, 1 accumulator, 0 - 4

# store player pos in reg 1 2

# initialize vars
rcrd 192
acc 8
to-mdc

# increase column
beqz-cf
inc*-reg 4

rot-rc
to-mdc
beqz 48