# catz <project:clitty modeule:2>

# Esolang Brainfuck(2) Interpreter Class
class Interpreter:
    def Brainfuck(self, code):
        if not any(x in code for x in set("><+-[].")):
            return None
        tape = [0] * 30000
        pointer, stack, loop_start, output = 0, [], {}, ""
        for i, char in enumerate(code):
            if char == "[":
                stack.append(i)
            elif char == "]":
                start = stack.pop()
                loop_start[start] = i
                loop_start[i] = start
        i = 0
        while i < len(code):
            char = code[i]
            if char == ">":
                pointer += 1
            elif char == "<":
                pointer -= 1
            elif char == "+":
                tape[pointer] += 1
            elif char == "-":
                tape[pointer] -= 1
            elif char == ".":
                output += chr(tape[pointer])
            # elif char == ",":
            #     tape[pointer] = ord(input("Input character: "))
            elif char == "[":
                if tape[pointer] == 0:
                    i = loop_start[i]
            elif char == "]":
                if tape[pointer] != 0:
                    i = loop_start[i]
            i += 1
        return output if any(c in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#+-' for c in output) else None

    def Pikalang(self, char):
        DICT_P = {
            "pi": "+",
            "ka": "-",
            "pika": "[",
            "chu": "]",
            "pipi": ">",
            "pichu": "<",
            "pikapi": ",",
            "pikachu": ".",
        }
        out = "".join([DICT_P.get(c, "") for c in char.split()])
        return self.Brainfuck(out)

    def Alphuck(self, char):
        DICT_AL = {
            "e": "+",
            "i": "-",
            "a": ">",
            "c": "<",
            "p": "[",
            "s": "]",
            "j": ".",
            "o": ",",
        }
        out = "".join([DICT_AL.get(c, "") for c in char.strip()])
        return self.Brainfuck(out)

    def ReverseFuck(self, char):
        DICT_REv = {
            "-": "+",
            "+": "-",
            "<": ">",
            ">": "<",
            "]": "[",
            "[": "]",
            ",": ".",
            ".": ",",
        }
        out = "".join([DICT_REv.get(c, "") for c in char.strip()])
        return self.Brainfuck(out)

    def Ooklang(self, char):
        DICT_OK = {
            "..": "+",
            "!!": "-",
            ".?": ">",
            "?.": "<",
            "!?": "[",
            "?!": "]",
            "!.": ".",
            ".!": ",",
        }
        char = "".join(char.replace("Ook", "").split())
        out = "".join(DICT_OK.get(char[i: i + 2], "")
                      for i in range(0, len(char), 2))
        return self.Brainfuck(out)

    def Blublang(self, char):
        DICT_Bl = {
            "..": "+",
            "!!": "-",
            ".?": ">",
            "?.": "<",
            "!?": "[",
            "?!": "]",
            "!.": ".",
            ".!": ",",
        }
        char = "".join(char.replace("Blub", "").split())
        out = "".join(DICT_Bl.get(char[i: i + 2], "")
                      for i in range(0, len(char), 2))
        return self.Brainfuck(out)

    def BinaryFuck(self, char):
        DICT_B = {
            "000": "+",
            "001": "-",
            "010": ">",
            "011": "<",
            "110": "[",
            "111": "]",
            "100": ".",
            "101": ",",
        }
        out = "".join(DICT_B.get(char[i: i + 3], "")
                      for i in range(0, len(char), 3))
        return self.Brainfuck(out)

    """
    # Morse Fuck Encoder Function
    def MorseFKE(self, char):
        DI_MORSENC = {"+": "..-","-": "-..",">": ".--","<": "--.","[": "---","]": "...",".": "-.-",",": ".-."}
        out = "".join([DI_MORSENC.get(c, "") for c in char.strip()])
        return out
    """

    def MorseFuck(self, char):
        DICTMF = {
            "..-": "+",
            "-..": "-",
            ".--": ">",
            "--.": "<",
            "---": "[",
            "...": "]",
            "-.-": ".",
            ".-.": ",",
        }
        out = "".join(DICTMF.get(char[i: i + 3], "")
                      for i in range(0, len(char), 3))
        return self.Brainfuck(out)


data = '++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>>+++++++++++++++.++.-----.'
s = Interpreter()
s1 = s.Brainfuck(data)
print(s1)

