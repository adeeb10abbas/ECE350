A = {'instruction_type': 'A-INSTRUCTION', 'value': '2', 'value_type': 'NUMBER', 'dest': 'null', 'jmp': 'null', 'status': 0}

#TODO
def generate_machine_code(program):
    """Generate machine code from intermediate data structure"""

    ram_counter = 0
    machine_code = []

    for instruction in program:
        if s['instruction_type'] == 'A-INSTRUCTION':
            address = ''
            if s['value'] in symbol_table:
                address = symbol_table[s['value']]

            else:
                symbol_table.update({s['value']: ram_counter})
                ram_counter += 1
                address = ram_counter

            bin = generate_A_binary(s, address)

        elif s['instruction_type'] == 'C-INSTRUCTION':
            C_bin = generate_C_binary(s)

        machine_code.append(bin)

    return machine_code

#TODO
def generate_A_binary(s, address):
    pass


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

C = {'instruction_type': 'C-INSTRUCTION', 'value': '', 'value_type': '', 'dest': 'M', 'comp': '0', 'jmp': 'null', 'status': 0} #what is the default if there isno jmp or comp?

#TOD0: Handle for when dest cmp and jmp are empty
def generate_C_binary(s):
    instruction = '111'
    dest = ''
    comp = ''
    jmp = ''

    if s['dest']:
        dest = valid_dest_patterns[s['dest']]
    else:
        dest =


    if s['comp']:
        comp = valid_comp_patterns[s['comp']]

    else:
        comp =

    if s['jmp'] and s['jmp'] != 'null':
        jmp = valid_dest_patterns[s['jmp']]
    else:
        jmp = 000

    print("dest", dest)
    print("comp", comp)
    print("jmp", jmp)

    instruction = instruction + comp + dest + jmp

    print("Instruction", instruction)
    return instruction



generate_C_binary(C)


# 111 0101010 001 000



# 111 0101010 001