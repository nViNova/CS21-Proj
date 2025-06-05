REG: dict[str, int] = {
    'RA': 0,  # 4 bits
    'RB': 0,
    'RD': 0,
    'RE': 0,
    'RC': 0,
    'ACC': 0,  # 4 bits
    'CF': 0,   # 1 bit
    'TEMP': 0, # 16 bits
}

NO_REGISTER_INST = {'rot-r', 'rot-l', 'rot-rc', 'rot-lc', 'from-mba', 'to-mba', 'from-mdc', 'to-mdc', 'addc-mba', 'add-mba', 'subc-mba', 'sub-mba', 'inc*-mba', 'dec*-mba', 'inc*-mdc', 'dec*-mdc'}
LENGTH_THREE = {'b-bit'}
START_END_INST = {'inc*-reg', 'dec*-reg', 'to-reg', 'from-reg'}
REG_ACC = {'to-reg', 'from-reg'}
TRIPLE_INPUT = {'b-bit'}
FOUR_BIT_IMM_SIXTEEN = {'add', 'sub', 'and', 'xor', 'or', 'r4'}
FOUR_BIT_IMM_EIGHT = {'acc'}
EIGHT_BIT_IMM_SIXTEEN = {'rarb', 'rcrd'}
ELEVEN_BIT_IMM_SIXTEEN = {'bnz-a', 'bnz-b', 'beqz', 'bnez', 'beqz-cf', 'bnez-cf', 'bnz-d'}
TWELVE_BIT_IMM_SIXTEEN = {'b', 'call'}



INST = {
    'rot-r':     '0x00',
    'rot-l':     '0x01',
    'rot-rc':    '0x02',
    'rot-lc':    '0x03',
    'from-mba':  '0x04',
    'to-mba':    '0x05',
    'from-mdc':  '0x06',
    'to-mdc':    '0x07',
    'addc-mba':  '0x08',
    'add-mba':   '0x09',
    'subc-mba':  '0x0A',
    'sub-mba':   '0x0B',
    'inc*-mba':  '0x0C',
    'dec*-mba':  '0x0D',
    'inc*-mdc':  '0x0E',
    'dec*-mdc':  '0x0F',
    'inc*-reg':  ('0x1', '0'),  
    'dec*-reg':  ('0x1', '1'),
    'and-ba':    '0x1A',
    'xor-ba':    '0x1B',
    'or-ba':     '0x1C',
    'and*-mba':  '0x1D',
    'xor*-mba':  '0x1E',
    'or*-mba':   '0x1F',
    'to-reg':    ('0x2', '0'),
    'from-reg':  ('0x2', '1'),
    'clr-cf':    '0x2A',
    'set-cf':    '0x2B',
    'ret':       '0x2E',
    'from-ioa':  '0x32',
    'inc':       '0x31',
    'bcd':       '0x36',
    'shutdown':  '0x373E',
    'nop':       '0x3E',
    'dec':       '0x3F',
    'add':       '0x40', 
    'sub':       '0x41', 
    'and':       '0x42', 
    'xor':       '0x43', 
    'or':        '0x44', 
    'r4':        '0x46', 
    'rarb':      ('0101', '0000'), 
    'rcrd':      ('0110', '0000'), 
    'acc':       '0x70',
    'b-bit':    '100',
    'bnz-a':    '10100',
    'bnz-b':    '10101',
    'beqz':     '10110',
    'bnez':     '10111',
    'beqz-cf':  '11000',
    'bnez-cf':  '11001',
    'bnz-d':    '11011',
    'b':        '1110',
    'call':     '1111',
}

