"""CPU functionality."""

import sys
# Codes

HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010

"""

Step 1: Add the constructor to cpu.py
Add list properties to the CPU class to hold 256 bytes of memory and 8 general-purpose registers.

Hint: you can make a list of a certain number of zeros with this syntax:

x = [0] * 25  # x is a list of 25 zeroes

"""


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.running = False

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

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

    def run(self):
        """Run the CPU."""
        # set running to True
        self.running = True
        while self.running:
            #  read memory address  stored in register pc
            ir = self.ram_read(self.pc)
            self.ram_read(self.pc)
            # store values from ram_read into variables in case they are needed.
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)
            self.trace()
            if ir == LDI:
                self.ldi(op_a, op_b)

            elif ir == PRN:
                self.prn(op_a, op_b)

            elif ir == HLT:
                self.hlt()

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def hlt(self):

        self.running = False
        self.pc += 1
        '''
        Implement HLT instruction handler, similar to exit() in python
        In run() in your if-else block, exit the loop if a HLT instruction is encountered, regardless of whether or not there are more lines of code in the LS-8 program you loaded.

        `HLT`
        Halt the CPU (and exit the emulator).

        Machine code:

        00000001 
        01

        '''
        pass

    def ldi(self, *operands):
        self.reg[operands[0]] = operands[1]
        self.pc += 3

        '''
        This instruction sets a specified register to a specified value.
        See the LS-8 spec for the details of what this instructions does 
        and its opcode value.

        Set the value of a register to an integer.
        Machine code:

        10000010 00000rrr iiiiiiii
        82 0r ii

        '''
        pass

    def prn(self, *operands):
        print(self.reg[operands[0]])
        self.pc += 2
        '''
        This is a very similar process to adding LDI, but the handler is simpler. See the LS-8 spec.
        At this point, you should be able to run the program and have it print 8 to the console!

        Print numeric value stored in the given register.

        Print to the console the decimal integer value that is stored in the given
        register.

        Machine code:

        01000111 00000rrr
        47 0r

        '''
        pass

    # Left off at step 7 in readme
