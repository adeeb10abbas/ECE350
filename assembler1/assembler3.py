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

def parse(filename):
    program = []
    rom_counter = 0

    cleaned_file = format_asm_file(filename) #removes whitespace, new line characters and comments and returns dictionary of lines with original line numbers
    if cleaned_file["status"] == -1:
        #print(f"error in line {cleaned_file['error_line']}")
        return f"error in line {cleaned_file['error_line']}"

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
    return program

def generate_machine_code(program):
    """Generate machine code from intermediate data structure"""

    ram_counter = 16
    machine_code = []

    for instruction in program:
        if instruction['instruction_type'] == 'A-INSTRUCTION':

            if instruction['value_type'] == 'NUMBER':
                number = int(instruction['value'])
                bin = generate_A_binary(number)

            elif instruction['value'] in symbol_table: #if its a number it won't be in the symbol table.
                address = symbol_table[instruction['value']]
                bin = generate_A_binary(address)

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

def print_intermediate_ds(intermediate_data_structure):
    print("Intermediate data structure: ")
    for instruction in intermediate_data_structure:
        print(instruction)

def print_machine_code(machine_code):
    for line in machine_code:
        print(line)


#Driver

# if __name__ == "__main__":
if len(sys.argv) < 2:
    print("Usage: assembler.py file-name.asm")
    print("Example: assembler.py mult.asm")

else:
    print("Assembling file:", sys.argv[1])
    print()
    file_name_minus_extension, _ = os.path.splitext(sys.argv[1])
    output_file = file_name_minus_extension + '.hack'
    # machine_code = run_assembler(sys.argv[1])
    try:
        intermediate_data_structure = parse(file_name)
        # if type(intermediate_data_structure) == str:
        #     print(intermediate_data_structure) #if error, returns error with line number
        #
        # else:
        #     print_intermediate_ds(intermediate_data_structure)
        #     machine_code = generate_machine_code(intermediate_data_structure)

            # if machine_code:
            #     print_machine_code(machine_code)
            #     print('Machine code generated successfully')
            #     print('Writing output to file:', output_file)
            #     f = open(output_file, 'w+')
            #     for s in machine_code:
            #         f.write('%s\n' %s)
            #     f.close()
            #
            # else:
            #     print("Error generating machine code")















