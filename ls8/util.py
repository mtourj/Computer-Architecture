def sanitize(line):
    '''
    Strip comments and empty spaces from text
    '''
    sep = ['\n', '#']

    for s in sep:
        i = line.find(s)
        if i >= 0:
            line = line[:i]
    return line.strip()

def set_bit(byte, position, value):
    set_value = 0

    # if value is truthy, but not a 1,
    # make sure it is a 1
    if value:
        set_value = 1

    mask = 1 << position

    return (byte & ~mask) | ((set_value << position) & mask)