"""CPU functionality."""

import sys
from util import set_bit

class CPU:
    """Main CPU class."""

    # LS8 instruction definitions
    HLT = 1
    RET = 17
    PUSH = 69
    POP = 70
    PRN = 71
    CALL = 80
    JMP = 84
    JEQ = 85
    JNE = 86
    LDI = 130
    ADD = 160
    MUL = 162
    CMP = 167

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.fl = 0b00000000
        self.ram = [00000000] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.dispatch = {}
        self.dispatch[self.HLT] = self.halt
        self.dispatch[self.LDI] = self.load_immediate
        self.dispatch[self.PRN] = self.sys_out
        self.dispatch[self.MUL] = self.mul
        self.dispatch[self.ADD] = self.add
        self.dispatch[self.PUSH] = self.push
        self.dispatch[self.POP] = self.pop
        self.dispatch[self.CALL] = self.call
        self.dispatch[self.RET] = self.ret
        self.dispatch[self.CMP] = self.cmp
        self.dispatch[self.JMP] = self.jmp
        self.dispatch[self.JNE] = self.jne
        self.dispatch[self.JEQ] = self.jeq

    def load(self, program):
        """Load a program into memory."""

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == self.CMP:
            self.fl = set_bit(self.fl, 2, self.reg[reg_a] < self.reg[reg_b])
            self.fl = set_bit(self.fl, 1, self.reg[reg_a] > self.reg[reg_b])
            self.fl = set_bit(self.fl, 0, self.reg[reg_a] == self.reg[reg_b])
        elif op == self.ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == self.MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):
        if address > len(self.ram):
            return 0
        return self.ram[address]

    def ram_write(self, address, data):
        self.ram[address] = data

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def halt(self):
        exit()

    def load_immediate(self):
        target_register = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[target_register] = value
        self.pc = self.pc + 3

    def sys_out(self):
        print(self.reg[self.ram_read(self.pc + 1)])
        self.pc = self.pc + 2

    def add(self):
        self.alu(self.ADD, self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
        self.pc = self.pc + 3

    def mul(self):
        self.alu(self.MUL, self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
        self.pc = self.pc + 3

    def push(self):
        self.reg[7] = self.reg[7] - 1
        self.ram_write(self.reg[7], self.reg[self.ram_read(self.pc + 1)])
        self.pc = self.pc + 2

    def pop(self):
        self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.reg[7])
        self.reg[7] = self.reg[7] + 1
        self.pc = self.pc + 2

    def call(self):
        self.reg[7] = self.reg[7] - 1
        self.ram_write(self.reg[7], self.pc + 2)
        self.pc = self.reg[self.ram_read(self.pc + 1)]

    def ret(self):
        self.pc = self.ram_read(self.reg[7])
        self.reg[7] = self.reg[7] + 1

    def cmp(self):
        self.alu(self.CMP, self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
        self.pc = self.pc + 3

    def jmp(self):
        self.pc = self.reg[self.ram_read(self.pc + 1)]

    def jne(self):
        # Value is 1 means 0b00000001 (`e` flag on)
        if self.fl != 1:
            self.pc = self.reg[self.ram_read(self.pc + 1)]
        else:
            self.pc = self.pc + 2

    def jeq(self):
        if self.fl == 1:
            self.pc = self.reg[self.ram_read(self.pc + 1)]
        else:
            self.pc = self.pc + 2

    def run(self):
        """Run the CPU."""

        running = True

        while running:
            ir = self.ram_read(self.pc)

            # We track the counter to make sure the
            # insutruction we ran moved the counter,
            # if it didn't, we advance to next instruction,
            # as per the spec
            old_counter = self.pc

            if ir not in self.dispatch:
                print('Bad instruction')
                self.trace()
                self.halt()

            self.dispatch[ir]()

            if self.pc == old_counter:
                self.pc = self.pc + 1
