# -*- coding: utf-8 -*-
"""Assembler for the Hack processor.

Author: Naga Kandasamy
Date created: August 8, 2020
Date modified: October 14, 2020

Student name(s): 
Date modified: 
"""

import os
import sys

"""The comp field is a c1 c2 c3 c4 c5 c6"""
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

"""Symbol table populated with predefined symbols and RAM locations"""
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

def print_intermediate_representation(ir):
    """Print intermediate representation"""
    
    for i in ir:
        print()
        for key, value in i.items():
            print(key, ':', value)

        
def print_instruction_fields(s):
    """Print fields in instruction"""
    
    print()
    for key, value in s.items():
        print(key, ':', value)

#
# def valid_tokens(s):
#     """Return True if tokens belong to valid instruction-field patterns"""
#
#     return True


def parse(command):
    """Implements finite automate to scan assembly statements and parse them.

    WHITE SPACE: Space characters are ignored. Empty lines are ignored.
    
    COMMENT: Text beginning with two slashes (//) and ending at the end of the line is considered 
    comment and is ignored.
    
    CONSTANTS: Must be non-negative and are written in decimal notation. 
    
    SYMBOL: A user-defined symbol can be any sequence of letters, digits, underscore (_), dot (.), 
    dollar sign ($), and colon (:) that does not begin with a digit.
    
    LABEL: (SYMBOL)
    """



    # Data structure to hold the parsed fields for the command
    s = {}
    s['instruction_type'] = ''
    s['value'] = ''
    s['value_type'] = ''
    s['dest'] = ''
    s['comp'] = ''
    s['jmp'] = ''
    s['status'] = 0
      
    return s    
   
def generate_machine_code():
    """Generate machine code from intermediate data structure"""
    
    machine_code = []
    
    return machine_code
    

def print_machine_code(machine_code):
    """Print generated machine code"""
    
    rom_address = 0
    for code in machine_code:
        print(rom_address, ':', code)
        rom_address = rom_address + 1


def run_assembler(file_name):

    """Pass 1: Parse the assembly code into an intermediate data structure.
    The intermediate data structure can be a list of elements, called ir, where
    each element is a dictionary 
    with the following structure: 
    
    s['instruction_type'] = ''
    s['value'] = ''
    s['value_type'] = ''
    s['dest'] = ''
    s['comp'] = ''
    s['jmp'] = ''
    s['status'] = 0
    
    The symbol table is also generated in this step.

    """
    
    """Pass 2: Generate the machine code from the intermediate data structure"""


    machine_code = []
    
    return machine_code




  
# if __name__ == "__main__":
if len(sys.argv) < 2:
    print("Usage: assembler.py file-name.asm")
    print("Example: assembler.py mult.asm")
else:
    print("Assembling file:", sys.argv[1])
    print()
    file_name_minus_extension, _ = os.path.splitext(sys.argv[1])
    output_file = file_name_minus_extension + '.hack'
    machine_code = run_assembler(sys.argv[1])
    if machine_code:
        print('Machine code generated successfully');
        print('Writing output to file:', output_file)
        f = open(output_file, 'w')
        for s in machine_code:
            f.write('%s\n' %s)
        f.close()
    else:
        print('Error generating machine code')
