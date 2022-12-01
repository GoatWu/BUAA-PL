import sys
import math
import random


class LuaInterpreter:
    def __init__(self, prog):
        self.prog = prog
        self.vars = {}
        self.error = 0
        self.pc = 0

    def check_func(self):
        pass

    def run(self):
        while True:
            if self.pc < len(self.prog):
                line = self.prog[self.pc]
            else:
                break

            print('DEBUG: ', line)

            op = line[0]
            if op == 'PRINT':
                plist = line[1]
                out = ""
                for label, val in plist:
                    if out:
                        out += " "
                    out += label
                    if val:
                        eval = self.eval(val)
                        out += str(eval)
                sys.stdout.write(out)
                sys.stdout.write("\n")
                sys.stdout.flush()

            self.pc += 1

    def add_statements(self, prog):
        for stat in prog:
            self.prog.append(stat)
