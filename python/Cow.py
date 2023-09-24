# -*- coding: utf-8 -*-
#!/usr/bin/env python3

# Python Interpreter for COW (Esolang)
# https://esolangs.org/wiki/COW

# Original Source:
# Author: Frank Buß
# COW JS implementation
# https://frank-buss.de/cow.html


class CowInterpreter:
    def __init__(self):
        self.output = ""
        self.memory = [0]
        self.cow_program = []
        self.position, self.mem_pos = 0, 0
        self.register_val = None

    def instructions(self, instruction):
        level = 0

        if instruction == 0:  # moo
            if self.position == 0:
                return False
            else:
                self.position -= 1  # skip previous command.
                level = 1
                while level > 0:
                    if self.position == 0:
                        break
                    self.position -= 1
                    if self.cow_program[self.position] == 0:
                        level += 1
                    elif self.cow_program[self.position] == 7:  # look for MOO
                        level -= 1
                if level != 0:
                    return False
                return self.instructions(self.cow_program[self.position])

        elif instruction == 1:  # mOo
            if self.mem_pos == 0:
                return False
            else:
                self.mem_pos -= 1

        elif instruction == 2:  # moO
            self.mem_pos += 1
            if self.mem_pos == len(self.memory):
                self.memory.append(0)

        elif instruction == 3:  # mOO
            if self.memory[self.mem_pos] == 3:
                return False
            else:
                return self.instructions(self.memory[self.mem_pos])

        elif instruction == 4:  # Moo
            if self.memory[self.mem_pos] != 0:
                self.output += chr(self.memory[self.mem_pos])
            else:
                self.memory[self.mem_pos] = ord(input("Enter a character")[0])

        elif instruction == 5:  # MOo
            self.memory[self.mem_pos] -= 1

        elif instruction == 6:  # MoO
            self.memory[self.mem_pos] += 1

        elif instruction == 7:  # MOO
            if self.memory[self.mem_pos] == 0:
                level = 1
                prev = 0
                # have to skip past next command when looking for next moo.
                self.position += 1
                if self.position == len(self.cow_program):
                    return False
                while level > 0:
                    prev = self.cow_program[self.position]
                    self.position += 1
                    if self.position == len(self.cow_program):
                        break
                    if self.cow_program[self.position] == 7:
                        level += 1
                    else:
                        # look for moo command.
                        if self.cow_program[self.position] == 0:
                            level -= 1
                            if prev == 7:
                                level -= 1
                if level != 0:
                    return False

        elif instruction == 8:  # OOO
            self.memory[self.mem_pos] = 0

        elif instruction == 9:  # MMM
            if self.register_val is None:
                self.register_val = self.memory[self.mem_pos]
            else:
                self.memory[self.mem_pos] = self.register_val
                self.register_val = None

        elif instruction == 10:  # OOM
            self.output += str(self.memory[self.mem_pos]) + "\n"

        # elif instruction == 11:  # oom
            # self.memory[self.mem_pos] = float(input("Please enter a number"))

        else:
            return False

        self.position += 1
        return True

    def run_cow(self, char):
        lang_char = ["moo", "mOo", "moO", "mOO", "Moo", "MOo", "MoO", "MOO", "OOO", "MMM", "OOM", "oom"]
        token = "   "
        for i in range(len(char)):
            token = token[1:] + char[i]
            for j in range(12):
                if token == lang_char[j]:
                    self.cow_program.append(j)
                    token = "   "
                    break

        while self.position != len(self.cow_program):
            if not self.instructions(self.cow_program[self.position]):
                break

        return self.output


cow_code = """
OOOMoOMoOMoOMoOMoOMoOMoOMoOMMMmoOMMMMMMmoOMMMMOOMOomOoMoOmoOmoomOoMMMmoOMMMMMMmoOMMMMOOMOo
mOoMoOmoOmoomOoMMMmoOMMMMMMmoOMMMMOOMOomOoMoOmoOmooOOOmoOOOOmOomOoMMMmoOMMMMOOMOomoOMoOmOo
moomoOMoOMoOMoOMoomOoOOOmoOOOOmOomOoMMMmoOMMMMOOMOomoOMoOmOomoomOomOoMMMmoOmoOMMMMOOMOomoO
MoOmOomoomoOMoOMoomOoOOOmoOOOOmOomOoMMMmoOMMMMOOMOomoOMoOmOomoomOomOoMMMmoOmoOMMMMOOMOomoO
MoOmOomoomOomOomOoMMMmoOmoOmoOMMMMOOMOomoOMoOmOomoomoOMoOMoOMoOMoOMoomOoOOOmoOOOOmOomOoMMM
moOMMMMOOMOomoOMoOmOomoomOomOoMMMmoOmoOMMMMOOMOomoOMoOmOomoomOomOomOoMMMmoOmoOmoOMMMMOOMOo
moOMoOmOomoomoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoomOo
"""

s = CowInterpreter()
data = s.run_cow(cow_code)
print(data)
