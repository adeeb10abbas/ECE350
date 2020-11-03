from format_asm_file import format_asm_file
from validate_instruction_types_h import validate_instruction
from machine_code import generate_C_binary, generate_A_binary

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
                return #todo

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

def generate_machine_code(program):
    """Generate machine code from intermediate data structure"""

    ram_counter = 15
    machine_code = []

    for instruction in program:
        if instruction['instruction_type'] == 'A-INSTRUCTION':
            if instruction['value'] in symbol_table:
                address = symbol_table[instruction['value']]

            else:
                #print(f"symbol not in symbol table. ram counter: ", ram_counter)
                symbol_table.update({instruction['value']: ram_counter})
                address = ram_counter
                ram_counter += 1

            bin = generate_A_binary(address)

        elif instruction['instruction_type'] == 'C-INSTRUCTION':
            bin = generate_C_binary(instruction)

        machine_code.append(bin)

    #print(machine_code)
    return machine_code

program = parse("mult.asm")
generate_machine_code(program)












