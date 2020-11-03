#TODO

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


def generate_machine_code(program):
    """Generate machine code from intermediate data structure"""

    ram_counter = 15
    machine_code = []

    for instruction in program:
        if instruction['instruction_type'] == 'A-INSTRUCTION':
            if instruction['value'] in symbol_table:
                address = symbol_table[instruction['value']]

            else:
                print(f"symbol not in symbol table. ram counter: ", ram_counter)
                symbol_table.update({instruction['value']: ram_counter})
                address = ram_counter
                ram_counter += 1

            bin = generate_A_binary(address)

        elif instruction['instruction_type'] == 'C-INSTRUCTION':
            bin = generate_C_binary(instruction)

        machine_code.append(bin)

    print(machine_code)
    return machine_code

A = {'instruction_type': 'A-INSTRUCTION', 'value': '2', 'value_type': 'NUMBER', 'dest': 'null', 'jmp': 'null', 'status': 0}

def generate_A_binary(address):
    instruction = '0' + f'{address:015b}'

    #print(instruction)
    return instruction



"""The dest bits are d1 d2 d3"""
valid_dest_patterns = {'null':'000',
                       'M':'001',
                       'D':'010',
                       'MD':'011',
                       'A':'100',
                       'AM':'101',
                       'AD':'110',
                       'AMD':'111'
                       }

valid_comp_patterns = {'0':'0101010',
                       '1':'0111111',
                       '-1':'0111010',
                       'D':'0001100',
                       'A':'0110000',
                       '!D':'0001101',
                       '!A':'0110001',
                       '-D':'0001111',
                       '-A':'0110011',
                       'D+1':'0011111',
                       'A+1':'0110111',
                       'D-1':'0001110',
                       'A-1':'0110010',
                       'D+A':'0000010',
                       'D-A':'0010011',
                       'A-D':'0000111',
                       'D&A':'0000000',
                       'D|A':'0010101',
                       'M':'1110000',
                       '!M':'1110001',
                       '-M':'1110011',
                       'M+1':'1110111',
                       'M-1':'1110010',
                       'D+M':'1000010',
                       'M+D':'1000010',
                       'D-M':'1010011',
                       'M-D':'1000111',
                       'D&M':'1000000',
                       'D|M':'1010101'
                       }

"""The jump fields are j1 j2 j3"""
valid_jmp_patterns =  {'null':'000',
                       'JGT':'001',
                       'JEQ':'010',
                       'JGE':'011',
                       'JLT':'100',
                       'JNE':'101',
                       'JLE':'110',
                       'JMP':'111'
                       }

#M = 1
C = {'instruction_type': 'C-INSTRUCTION', 'value': '', 'value_type': '', 'dest': 'M', 'comp': '1', 'jmp': 'null', 'status': 0} #what is the default if there isno jmp or comp?

#dest=comp;jmp
def generate_C_binary(s):
    instruction = '111'

    dest = valid_dest_patterns[s['dest']]
    comp = valid_comp_patterns[s['comp']]
    jmp = valid_dest_patterns[s['jmp']]

    instruction = instruction + comp + dest + jmp

    #print("Instruction", instruction)
    return instruction

program = [A, C]

generate_machine_code(program)



print("15 in bin", bin(15))