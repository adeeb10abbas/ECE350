from format_asm_file import format_asm_file
from validate_instruction_types_h import validate_instruction

symbol_table = {'SP':0,
                'LCL':1,
                'ARG':2,
                'THIS':3,
                'THAT':4,
                'R0':0,
                'R1':1,
                'R2':2,
                'R3':3,
                'R4':4,
                'R5':5,
                'R6':6,
                'R7':7,
                'R8':8,
                'R9':9,
                'R10':10,
                'R11':11,
                'R12':12,
                'R13':13,
                'R14':14,
                'R15':15,
                'SCREEN':16384,
                'KBD':24576
                }

"""
File is converted to a dictionary of this type:
{"status": 0 if no errors, -1 if error, 
"line_error": line_number of error,
line_number: command 

where line_number is a line number in the original file that is not a comment 

"""
def parse(filename):
    program = []
    rom_counter = 0

    cleaned_file = format_asm_file(filename) #removes whitespace, new line characters and comments and returns dictionary of lines with original line numbers
    if cleaned_file["status"] == -1:
        print(f"error in line {cleaned_file['error_line']}")
        return cleaned_file #IF ERR, RETURNS DICT WITH

    else:
        cleaned_file.pop('status')
        cleaned_file.pop('error_line')

        for line_number in cleaned_file.keys():
            #print(cleaned_file[line_number])

            s = validate_instruction(cleaned_file[line_number]) #s is the data structure

            if s["status"] == -1:
                print(f'Error on line {line_number}')
                break

            elif s["status"] == 0:
                if s["instruction_type"] == "A-INSTRUCTION" or \
                        s["instruction_type"] == "C-INSTRUCTION":
                    rom_counter += 1
                    program.append(s)

                elif s["instruction_type"] == 'LABEL':
                    if s["value"] not in symbol_table:
                        symbol_table.update({s["value"]: rom_counter}) #TODO: What should the ROM counter count be?
                    else:
                        continue

        # print("We have our data structure")
        # print("Program: ", program)

    return program

            #elif status is something else to handle for xyz


program = parse("mult.asm")

# TEST

f = open("test_f", "w+")
#program = [{'instruction_type': 'A-INSTRUCTION', 'value': '2', 'value_type': 'NUMBER', 'dest': 'null', 'jmp': 'null', 'status': 0}, {'instruction_type': 'C-INSTRUCTION', 'value': '', 'value_type': '', 'dest': 'M', 'comp': '0', 'jmp': 'null', 'status': 0}, {'instruction_type': 'A-INSTRUCTION', 'value': '1', 'value_type': 'NUMBER', 'dest': 'null', 'jmp': 'null', 'status': 0}, {'instruction_type': 'C-INSTRUCTION', 'value': '', 'value_type': '', 'dest': 'D', 'comp': 'M', 'jmp': 'null', 'status': 0}, {'instruction_type': 'A-INSTRUCTION', 'value': 'END', 'value_type': 'SYMBOL', 'dest': '', 'jmp': '', 'status': 0}, {'instruction_type': 'C-INSTRUCTION', 'value': '', 'value_type': '', 'dest': '', 'comp': 'D', 'jmp': 'JEQ', 'status': 0}, {'instruction_type': 'A-INSTRUCTION', 'value': '0', 'value_type': 'NUMBER', 'dest': 'null', 'jmp': 'null', 'status': 0}, {'instruction_type': 'C-INSTRUCTION', 'value': '', 'value_type': '', 'dest': 'D', 'comp': 'M', 'jmp': 'null', 'status': 0}, {'instruction_type': 'A-INSTRUCTION', 'value': '2', 'value_type': 'NUMBER', 'dest': 'null', 'jmp': 'null', 'status': 0}, {'instruction_type': 'C-INSTRUCTION', 'value': '', 'value_type': '', 'dest': 'M', 'comp': 'M+D', 'jmp': 'null', 'status': 0}, {'instruction_type': 'A-INSTRUCTION', 'value': '1', 'value_type': 'NUMBER', 'dest': 'null', 'jmp': 'null', 'status': 0}, {'instruction_type': 'C-INSTRUCTION', 'value': '', 'value_type': '', 'dest': 'M', 'comp': 'M-1', 'jmp': 'null', 'status': 0}, {'instruction_type': 'A-INSTRUCTION', 'value': 'BEGIN', 'value_type': 'SYMBOL', 'dest': '', 'jmp': '', 'status': 0}, {'instruction_type': 'C-INSTRUCTION', 'value': '', 'value_type': '', 'dest': '', 'comp': '0', 'jmp': 'JMP', 'status': 0}, {'instruction_type': 'A-INSTRUCTION', 'value': 'END', 'value_type': 'SYMBOL', 'dest': '', 'jmp': '', 'status': 0}, {'instruction_type': 'C-INSTRUCTION', 'value': '', 'value_type': '', 'dest': '', 'comp': '0', 'jmp': 'JMP', 'status': 0}]

for d in program:
    f.write(f"{d} + \n")
print(symbol_table)












