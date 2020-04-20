"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    # LS8 instruction definitions
    HLT = 1
    LDI = 130
    PRN = 71
    MUL = 162

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [00000000] * 256
        self.reg = [0] * 8

    def load(self, program):
        """Load a program into memory."""

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
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
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        
        running = True

        while running:
            ir = self.ram_read(self.pc)

            if ir == self.HLT:
                running = False
            elif ir == self.LDI:
                target_register = self.ram_read(self.pc + 1)
                value = self.ram_read(self.pc + 2)
                self.reg[target_register] = value
                self.pc = self.pc + 3
            elif ir == self.PRN:
                print(self.reg[self.ram_read(self.pc + 1)])
                self.pc = self.pc + 2
            elif ir == self.MUL:
                self.alu('MUL', self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
                self.pc = self.pc + 3
            else:
                print('Bad instruction')
                self.trace()
                running = False