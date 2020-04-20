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
