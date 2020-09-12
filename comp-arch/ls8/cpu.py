# Definitions
# IR - Instruction Register, contains a copy of the currently executing instruction
# MAR - Memory Address Register, holds the memory address we're reading or writing
# MDR - Memory Data Register, holds the value to write or the value just read
"""CPU functionality."""

import sys

# Day 1 Step 4-6

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Day 1 Step 1
        self.br_tbl = {}
        # hold 256 bytes of memory
        self.ram = [0] * 256
        # hold 8 general-purpose registers
        self.reg = [0] * 8
        # Program Counter
        self.pc = 0

        # Instructions
        # Halt the CPU (and exit the emulator).
        self.br_tbl[HLT] = self.hlt_func
        # load "immediate", store a value in a register, or "set this register to this value".
        self.br_tbl[LDI] = self.ldi_func
        # a pseudo-instruction that prints the numeric value stored in a register.
        self.br_tbl[PRN] = self.prn_func
        # Multiply the values in two registers together and store the result in register1.
        self.br_tbl[MUL] = self.mul_func
        # Push the value in the given register on the stack
        self.br_tbl[PUSH] = self.push_func
        # Pop the value in the stack into the given register
        self.br_tbl[POP] = self.pop_func

    # Day 1 Step 2
    # Ram read should accept the address to read and
    # Return the value stored there

    def ram_read(self, MAR):
        return self.ram[MAR]

    # Ram write should accept a value to write and
    # the address to write it to
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    # Day 2 Step 7
    def load(self):
        """Load a program into memory."""
        # Load the program file
        try:
            address = 0

            # if we don't specify a file at all. originally throws error, list index out of range
            # describe how to use this program
            if len(sys.argv) != 2:
                print("Usage: comp.py progname")
                sys.exit(0)

            # from input in terminal, python ls8.py examples/mult.ls8
            with open(f'{sys.argv[1]}') as f:
                for line in f:
                    # line and temp is not necessary, but a 'just in case'
                    line0 = line.split('#')
                    temp = line0[0].strip()
                    # if line is empty
                    # if len(temp) == 0:
                    #     continue
                    # # if temp at 0 is a hashmark
                    # if temp[0] == "#":
                    #     continue
                    #     # temp = line.split('#')
                    #     # using base 2, decimal
                    self.ram[address] = int(temp, 2)
                    address += 1
                    # to handle errors such as comments, blanklines, etc.
        except ValueError:
            print(f"Invalid number: {temp[0]}")
            sys.exit(1)
        # check validity, comes from the command line "Thinking like a villan"
        except FileNotFoundError:
            print(f"Couldn't open {sys.argv[1]}")
            sys.exit(3)

            # print first 12 address
            # print(self.ram[:12])
            sys.exit(2)

            # valid check if there is no instructions
            if address == 0:
                print("Program was empty!")
                sys.exit(4)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            result = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = result
            self.pc += 3
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

    # Day 1 Step 4: Implement the HLT instruction handler
    def hlt_func(self):
        exit(1)

    def ldi_func(self):
        MAR = self.ram_read(self.pc + 1)
        MDR = self.ram_read(self.pc + 2)

        if MAR < len(self.ram):
            self.reg[MAR] = MDR
        # Increment program counter by 3 steps inside the RAM
        self.pc += 3

    def prn_func(self):
        operand_a = self.ram_read(self.pc + 1)
        print(self.reg[operand_a])
        self.pc += 2

    # Day 2 Step 8: Implement a Multiply and Print the Result
    def mul_func(self):
        reg_a = self.ram_read(self.pc + 1)
        # register 2
        reg_b = self.ram_read(self.pc + 2)
        self.alu("MUL", reg_a, reg_b)

    # Step 10: Implement System Stack
    def push_func(self):
        # Decrement the stack pop_func
        self.reg[7] -= 1
        operand_a = self.ram_read(self.pc + 1)
        # Store value from reg to ram
        self.ram[self.reg[7]] = self.reg[operand_a]
        self.pc += 2

    # Step 11: Implement Subroutine Calls
    def ret_func

    # Step 10: Implement System Stack
    def pop_func(self):
        # Read value of SP, overwrite next register
        operand_a = self.ram_read(self.pc + 1)
        self.reg[operand_a] = self.ram_read(self.reg[7])
        # Increment SP
        self.reg[7] += 1
        self.pc += 2

    # Day 1 Step 3

    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running == True:

            IR = self.ram[self.pc]
            # # Loading
            # # if IR == 0b10000010:
            # if IR == LDI:
            #     operand_a = self.ram[self.pc + 1]
            #     operand_b = self.ram[self.pc + 2]
            #     self.reg[operand_a] = operand_b
            #     self.pc += 3  # 3 movements
            # # elif IR == 0b01000111:
            # elif IR == PRN:
            #     operand_a = self.ram[self.pc + 1]
            #     value = self.reg[operand_a]
            #     print(value)
            #     self.pc += 2
            # # elif IR == 0b00000001:
            # elif IR == HLT:
            #     self.running = False
            # # elif IR == 0b10100010:
            # elif IR == MUL:
            #     print("This is MUlt_Func")
            #     # register 1
            #     register1 = self.ram_read(self.pc + 1)
            #     # register 2
            #     register2 = self.ram_read(self.pc + 2)

            #     self.reg[register1] = self.reg[register1] * self.reg[register2]
            #     self.pc += 3

            # elif IR == PUSH:
            #     self.reg[7] -= 1
            #     operand_a = self.ram_read(self.pc + 1)
            #     self.ram[self.reg[7]] = self.reg[operand_a]
            # print("IR: ", IR)
            if IR in self.br_tbl:
                # find the function/instruction based on the IR
                self.br_tbl[IR]()
            else:
                print("CAN'T FiND", IR)
