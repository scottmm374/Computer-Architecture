"""CPU functionality."""

import sys


### Registers ###
R0 = 0x00
R1 = 0x01
R2 = 0x02
R3 = 0x03
R4 = 0x04
R5 = 0x05
R6 = 0x06
R7 = 0x07
PROGRAM_END = 0x04
SP = 0x07
STACK_HEAD = 0xf4
DONE = 0

# Other
MUL = 0b10100010
CALL = 0b01010000
RET = 0b00010001
PUSH = 0b01000101
POP = 0b01000110
PRN = 0b01000111
HLT = 0b00000001
LDI = 0b10000010
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
CMP = 0b10100111
DONE = 0
UNKNOWN_INSTRUCTION = 1
IO_ERROR = 2
STACK_OVERFLOW = 3

### Bit Tools ###
ONE_BYTE = 0xff
ONE_BIT = 0x01
OP_SETS_INST = 0x04
NUM_OPERANDS = 0x06


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[SP] = STACK_HEAD
        self.pc = 0x00
        self.fl = 0x00

        self.perform_op = {}
        self.perform_op[LDI] = self._ldi
        self.perform_op[PRN] = self._prn
        self.perform_op[HLT] = self._hlt
        self.perform_op[MUL] = self._mul
        self.perform_op[PUSH] = self._push
        self.perform_op[POP] = self._pop
        self.perform_op[JMP] = self._jmp
        self.perform_op[JEQ] = self._jeq
        self.perform_op[JNE] = self._jne
        self.perform_op[CMP] = self._cmp

        self.is_running = False

    def _cmp(self, *operands):
        # compare values in reg A and reg B
        self.alu("CMP", *operands)

    def _jmp(self, *operands):
        # JMP register
        # Jump to the address stored in the given register."""
        self.pc = self.reg[operands[0]]

    def _jeq(self, *operands):
        # JEQ register
        if self.fl & 0x01:
            self.pc = self.reg[operands[0]]
        else:
            self.pc += 2

    def _jne(self, *operands):
        # JNE register
        # If E flag is clear jump to address in register.
        if not (self.fl & 0x01):
            self.pc = self.reg[operands[0]]
        else:
            self.pc += 2

    def _ldi(self, *operands):
        # Set the value of a register to an integer.

        self.reg[operands[0]] = operands[1]

    def _prn(self, *operands):
        """PRN registerA
        Print numeric value stored in the given register."""
        print(self.reg[operands[0]])

    def _hlt(self, *operands):
        """HLT
        Halt the CPU (and exit the emulator)."""

        self.is_running = False

    def _mul(self, *operands):
        """MUL registerA registerB
        Multiply the values in two registers together and store the result in registerA."""

        self.alu("MUL", *operands)

    def _pop(self, *operands):
        """POP registerA
        Pop the value at the top of the stack into the given register."""

        self.reg[operands[0]] = self.ram_read(self.reg[SP])
        if self.reg[SP] < STACK_HEAD:
            self.reg[SP] += 1

    def _push(self, *operands):
        """PUSH registerA
        Push the value in the given register on the stack."""

        if (self.reg[SP]-1) >= self.reg[PROGRAM_END]:
            self.reg[SP] -= 1
            self.ram_write(self.reg[SP], self.reg[operands[0]])
        else:
            print(f"Stack Overflow!!")
            self.trace()
            self._shutdown(STACK_OVERFLOW)

    def load(self, program_path):
        """Load a program into memory."""
        address = 0

        try:
            with open(program_path) as program:
                for line in program:
                    split_line = line.split("#")
                    instruction = split_line[0].strip()
                    if instruction != "":
                        self.ram[address] = int(instruction, 2)
                        address += 1
        except:
            print(f"Cannot open file at \"{program_path}\"")
            self._shutdown(IO_ERROR)

        # store end of program into PROGRAM_END register
        self.reg[PROGRAM_END] = address

    def _to_next_instruction(self, ir):

        isPcAlreadySet = ir >> 0x04
        isPcAlreadySet = isPcAlreadySet & 0xff
        if not isPcAlreadySet:
            self.pc += (ir >> 0x06) + 1

    def _shutdown(self, exit_code=0):
        print("Shutting Down...")
        sys.exit(exit_code)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b] & 0xff

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def run(self):
        """Run the CPU."""
        print("Running...")
        self.is_running = True
        while self.is_running:
            instruction_reg = self.ram_read(self.pc)
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)

            if instruction_reg in self.perform_op:
                self.perform_op[instruction_reg](op_a, op_b)
                self._to_next_instruction(instruction_reg)
            else:
                print(f"Unknown Instruction {instruction_reg}")
                self._shutdown(UNKNOWN_INSTRUCTION)

        self._shutdown()
