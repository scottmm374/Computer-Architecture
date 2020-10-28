#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load()

"""
run()
 workhorse of the processor. 
reads memory address stored in register PC
then store result in IR (instruction register)
Can be local variable in run()
Some instructions requires up to the next two bytes of data after the PC in memory to perform operations on. Sometimes the byte value is a register number, other times it's a constant value (in the case of LDI). Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case the instruction needs them.

Then, depending on the value of the opcode, perform the actions needed for the instruction per the LS-8 spec. Maybe an if-elif cascade...? There are other options, too.

After running code for any particular instruction, the PC needs to be updated to point to the next instruction for the next iteration of the loop in run(). The number of bytes an instruction uses can be determined from the two high bits (bits 6-7) of the instruction opcode. See the LS-8 spec for details.
"""

cpu.run()
