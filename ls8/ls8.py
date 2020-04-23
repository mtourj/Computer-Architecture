#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
from util import sanitize

if len(sys.argv) != 2:
    print("Usage: python ls8.py <program location>")
    exit()

program_location = sys.argv[1]

program = []

with open(program_location, 'r') as program_file:
    data = program_file.readlines()

    for line in data:
        raw = sanitize(line)

        if len(raw) > 0:
            program.append(int(sanitize(line), 2))

cpu = CPU()

cpu.load(program)
cpu.run()
