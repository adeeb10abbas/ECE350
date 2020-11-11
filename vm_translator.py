# -*- coding: utf-8 -*-
"""
Compiler back end for the Hack processor.
Translates from a stack-based language for the virtual machine to the Hack assembly 

Author: Naga Kandasamy
Date created: September 1, 2020

Student name(s): 
Date modified: 
"""
import os
import sys

## To do paraphrase

def generate_exit_code():
    """Generate some epilogue code that places the program, upon completion, into 
    an infinite loop. 
    """
    s = []
    s.append('(THATS_ALL_FOLKS)')
    s.append('@THATS_ALL_FOLKS')
    s.append('0;JMP')
    return s


def generate_push_code(segment, index):
    """Generate assembly code to push value into the stack.
    In the case of a variable, it is read from the specified memory segment using (base + index) 
    addressing.
    """
    similar_segments1 = [
        'this',
        'that',
        'local',
        'argument'
    ]
    similar_segments2 = [
        'temp',
        'pointer',
    ]

    s = []
    if segment == "constant":
        s.append("@"+str(index))
        s.append("D=A")
        s.append("@SP")
        s.append("A=M")
        s.append("M=D")
        s.append("@SP")
        s.append("M=M+1")

    elif segment == "static": #TODO
        s.append("@"+str(index)) ## make sure this is correct not entirely sure (@filename.{index})
        s.append("D=M")
        s.append("@SP")
        s.append("A=M")
        s.append("M=D")
        s.append("@SP")
        s.append("M=M+1")

    elif segment in similar_segments1:
        s.append("@" + str(index))
        s.append("D=A")

        if segment == 'argument':
            s.append("@ARG")
        elif segment == 'local':
            s.append("@LCL")
        elif segment == 'this':
            s.append("@THIS")
        elif segment == 'that':
            s.append("@THAT")

        s.append("A=M+D")
        s.append("D=M")
        s.append("@SP")
        s.append("A=M")
        s.append("M=D")
        s.append("@SP")
        s.append("M=M+1")

    elif segment in similar_segments2:
        s.append("@" + str(index))  # get value into D
        s.append("D=A")

        if segment == 'temp':
            s.append("@5")
        elif segment == 'pointer':
            s.append("@3")

        s.append("A=A+D")
        s.append("D=M")
        s.append("@SP")  # put it onto the stack
        s.append("A=M")
        s.append("M=D")
        s.append("@SP")  # increment the stack pointer
        s.append("M=M+1")

    else:
        print("Error Segment is not [local, argument, this, that, temp, pointer, and static segments.]")

    return s


def generate_pop_code(segment, index):
    """Generate assembly code to pop value from the stack.
    The popped value is stored in the specified memory segment using (base + index) 
    addressing.
    """
    s = []
    similar_segments1 = [
        'this',
        'that',
        'local',
        'argument'
    ]
    
    if segment == "static":
        s.append("@SP")
        s.append("M=M-1")
        s.append("A=M")
        s.append("D=M")
        s.append(f"@{index}")
        s.append("M=D")

    elif segment == "pointer":
        s.append("@" + index)
        s.append("D=A")
        s.append("@3")
        s.append("D=A+D")
        s.append("@R13")
        s.append("M=D")
        s.append("@SP")
        s.append("M=M-1")
        s.append("A=M")
        s.append("D=M")
        s.append("@R13")
        s.append("A=M")
        s.append("M=D")

                            #TODO: Why do we not save temp as a memory segment?
    elif segment == "temp": #TODO: OH Question, why do we have temp segment and 2 general purpose registers?
        s.append(f"@{index}")
        s.append("D=A")
        s.append("@5")
        s.append("D=D+A")
        s.append("@R13")
        s.append("M=D")
        s.append("@SP")
        s.append("M=M-1")
        s.append("A=M")
        s.append("D=M")
        s.append("@R13")
        s.append("A=M")
        s.append("M=D")

    elif segment in similar_segments1:
        if segment == 'local':
            s.append("@LCL")
        elif segment == 'this':
            s.append("@THIS")
        elif segment == 'that':
            s.append("@THAT")
        elif segment == 'argument':
            s.append("@ARG")

        s.append("D=M")
        s.append(f"@{index}")
        s.append("D=D+A")
        s.append("@R13") #TODO: Is R13 temp register for sure?
        s.append("M=D")
        s.append("@SP")
        s.append("M=M-1")
        s.append("A=M")
        s.append("D=M")
        s.append("@R13")
        s.append("A=M")
        s.append("M=D")

    else:
        print("Error Segment is not [local, argument, this, that, temp, pointer, and static segments.]")

    return s


def generate_arithmetic_or_logic_code(operation):
    """Generate assembly code to perform the specified ALU operation. 
    The two operands are popped from the stack and the result of the operation 
    placed back in the stack.
    """
    s = []
    similar_operations = ['add', 'sub', 'or', 'and']

    if operation in similar_operations:
        s.append("@SP")
        s.append("M = M - 1")
        s.append("A = M")
        s.append("D = M")
        s.append("@SP")
        s.append("M = M - 1")
        s.append("A = M")

        if operation == 'add':
            s.append("D = M+D")
        elif operation == 'sub':
            s.append("D = M-D")
        elif operation == 'or':
            s.append('D = D|M')
        elif operation == 'and':
            s.append('D = D&M')

        s.append("@SP")
        s.append("A = M")
        s.append("M = D")

        #adjust stack pointer
        s.append("@SP")
        s.append("M = M + 1")

    else:
        print("Error Message") #TODO: Error message

    return s


def generate_unary_operation_code(operation):
    """Generate assembly code to perform the specified unary operation. 
    The operand is popped from the stack and the result of the operation 
    placed back in the stack.
    """
    #Instead of popping and then pushing, we just negated and not-ed in place. Stack pointer does not change.
    s = []
    s.append("@SP")
    s.append("A=M-1")

    if operation == "neg":
        s.append("M=-M")

    elif operation == "not":
        s.append("M=!M")

    else:
        print("Error message") #TODO: Error message
    
    return s


def generate_relation_code(operation, line_number):
    """Generate assembly code to perform the specified relational operation. 
    The two operands are popped from the stack and the result of the operation 
    placed back in the stack.
    """

    s = []
    label_1 = ''
    label_2 = ''

    s.append('@SP')
    s.append('M=M-1')
    s.append('A=M')
    s.append('D=M')  # D  = operand2
    s.append('@SP')
    s.append('M=M-1')  # Adjust stack pointer
    s.append('A=M')
    s.append('D=M-D')  # D = operand1 - operand2
    label_1 = 'IF_T_' + str(line_number)
    s.append('@' + label_1)

    # jump to label1 if D = 0, D < 0 and D > 0
    if operation == 'eq':
        s.append('D;JEQ')

    elif operation == 'lt':
        s.append('D;JLT')  # if operand1 < operand2 goto IF_LT_*

    elif operation == 'gt':
        s.append('D;JGT')

    s.append('@SP')
    s.append('A=M')
    s.append('M=0')  # Save result on stack
    label_2 = 'END_IF_ELSE_' + str(line_number)
    s.append('@' + label_2)
    s.append('0;JMP')
    s.append('(' + label_1 + ')')
    s.append('@SP')
    s.append('A=M')
    s.append('M=-1')  # Save result on stack
    s.append('(' + label_2 + ')')
    s.append("@SP")
    s.append("M=M+1")

    return s
  

def generate_if_goto_code(label):
    """Generate code for the if-goto statement. 

    Behavior:
    
    1. Pop result of expression from stack.
    2. If result is non-zero, goto (LABEL).
    
    Example:
    
    if (expression) 
        S1
    else
        S2
    
    VM code: 
    
        // Code to evaluate expression and place result in stack
        // if-goto L1
        // Code to execute S2
        // goto L2
        // (L1)
        // Code to execute S1
        // (L2)
        // Rest of code
    
    """
    s = []

    s.append("@SP")
    s.append("M=M-1")
    s.append("A=M")
    s.append("D=M")
    s.append(f"@{label}")
    s.append("D;JNE")

    return s


def generate_goto_code(label):
    """Generate assembly code for goto."""
    s = []

    s.append(f"@{label}")
    s.append("0;JMP")

    return s

def generate_pseudo_instruction_code(label):
    """Generate the pseudo-instruction for label."""
    s = []
    s.append('(' + label + ')')
    return s

def generate_set_code(register, value):
    """Generate assembly code for set"""
    s = []
    
    s.append('@' + value)
    s.append('D=A')
    
    if register == 'sp':
        s.append('@SP')
    
    elif register == 'local':
        s.append('@LCL')
    
    elif register == 'argument':
        s.append('@ARG')
        
    elif register == 'this':
        s.append('@THIS')
        
    elif register == 'that':
        s.append('@THAT')
        
    s.append('M=D')
    
    return s

def translate(tokens, line_number):
    """Translate a VM command/statement into the corresponding Hack assembly commands/statements."""
    s = []
    
    if tokens[0] == 'push':
        s = generate_push_code(tokens[1], tokens[2])    # Generate code to push into stack
        
    elif tokens[0] == 'pop':
        s = generate_pop_code(tokens[1], tokens[2])     # Generate code to pop from stack
        
    elif tokens[0] == 'add' or tokens[0] == 'sub' \
         or tokens[0] == 'mult' or tokens[0] == 'div' \
         or tokens[0] == 'or' or tokens[0] == 'and':
        s = generate_arithmetic_or_logic_code(tokens[0])  # Generate code for ALU operation
        
    elif tokens[0] == 'neg' or tokens[0] == 'not':
        s = generate_unary_operation_code(tokens[0])    # Generate code for unary operations
        
    elif tokens[0] == 'eq' or tokens[0] == 'lt' or tokens[0] == 'gt':
        s = generate_relation_code(tokens[0], line_number)
    
    elif tokens[0] == 'label':
        s = generate_pseudo_instruction_code(tokens[1])
    
    elif tokens[0] == 'if-goto':
        s = generate_if_goto_code(tokens[1]) 
        
    elif tokens[0] == 'goto':
        s = generate_goto_code(tokens[1])
    
    elif tokens[0] == 'set':
        s = generate_set_code(tokens[1], tokens[2])
    
    elif tokens[0] == 'end':
        s = generate_exit_code() #TODO: Exit code generation
        
    else:
        print('translate: Unknown operation')           # Unknown operation 
    
    return s

def run_vm_translator(file_name):
    """Main translator code. """
    assembly_code = []
    line_number = 1
    
    with open(file_name, 'r') as f:
        for command in f:        
            # print("Translating line:", line_number, command)
            tokens = (command.rstrip('')).split()
            
            # Ignore blank lines
            if not tokens:
                continue            
            
            if tokens[0] == '//':
                continue                                # Ignore comment

            else:
                s = translate(tokens, line_number)
                line_number = line_number + 1
            
            if s:
                for i in s:
                    assembly_code.append(i)
            else:
                assembly_code = []
                # return assembly_code
    
    return assembly_code


# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: Python vm_translator.py file-name.vm")
#         print("Example: Python vm_translator.py mult.vm")
#     else:
#         print("Translating VM file:", sys.argv[1])
#         print()
#         file_name_minus_extension, _ = os.path.splitext(sys.argv[1])
#         output_file = file_name_minus_extension + '.asm'
#         assembly_code = run_vm_translator(sys.argv[1])
#         if assembly_code:
#             print('Assembly code generated successfully');
#             print('Writing output to file:', output_file)
#             f = open(output_file, 'w')
#             for s in assembly_code:
#                 f.write('%s' %s)
#             f.close()
#         else:
#             print('Error generating assembly code')