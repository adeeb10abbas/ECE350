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
    s = []
    if segment=="constant":
        s.append("@"+str(index))
        s.append("D=A")
        s.append("@SP")
        s.append("A=M")
        s.append("M=D")
        s.append("@SP")
        s.append("M=M+1")

    elif segment == "static":
        s.append("@"+str(index)) ## make sure this is correct not entirely sure (@filename.{index})
        s.append("D=M")
        s.append("@SP")
        s.append("A=M")
        s.append("M=D")
        s.append("@SP")
        s.append("M=M+1")

    elif segment == "this":
        s.append("@"+str(index))
        s.append("D=A")
        s.append("@THIS")
        s.append("A=M+D")
        s.append("D=M")
        s.append("@SP")
        s.append("A=M")
        s.append("M=D")
        s.append("@SP")
        s.append("M=M+1")

    elif segment == "that":
        s.append("@" + str(index)) # get value into D
        s.append("D=A")
        s.append("@THAT")
        s.append("A=M+D") 
        s.append("D=M")
        s.append("@SP") # put it onto the stack
        s.append("A=M")
        s.append("M=D")
        s.append("@SP") # increment the stack pointer
        s.append("M=M+1")

    elif segment =="local":
        s.append("@" + str(index)) # get value into D
        s.append("D=A")
        s.append("@LCL")
        s.append("A=M+D") 
        s.append("D=M")
        s.append("@SP") # put it onto the stack
        s.append("A=M")
        s.append("M=D")
        s.append( "@SP") # increment the stack pointer
        s.append("M=M+1")

    elif segment =="temp":
        s.append("@" + str(index)) # get value into D
        s.append("D=A")
        s.append("@5")
        s.append("A=A+D") 
        s.append("D=M")
        s.append("@SP") # put it onto the stack
        s.append("A=M")
        s.append("M=D")
        s.append("@SP") # increment the stack pointer
        s.append("M=M+1")

    elif segment =="argument":
        s.append("@" + str(index)) # get value into D
        s.append("D=A")
        s.append("@ARG")
        s.append("A=M+D") 
        s.append("D=M")
        s.append("@SP") # put it onto the stack
        s.append( "A=M")
        s.append("M=D")
        s.append("@SP") # increment the stack pointer
        s.append("M=M+1")

    elif segment =="pointer":
        s.append("@" + str(index)) # get value into D
        s.append("D=A")
        s.append("@3")
        s.append("A=A+D") 
        s.append("D=M")
        s.append("@SP") # put it onto the stack
        s.append("A=M")
        s.append("M=D")
        s.append("@SP") # increment the stack pointer
        s.append("M=M+1")

    else: 
        print("Error Segment is not [local, argument, this, that, temp, pointer, and static segments.]")
        # FIXME: complete implmentation for local, argument, this, that, temp, pointer, and static segments.
    return s
    

def generate_pop_code(segment, index):
    """Generate assembly code to pop value from the stack.
    The popped value is stored in the specified memory segment using (base + index) 
    addressing.
    """
    s = []
    
    # FIXME: complete implmentation for local, argument, this, that, temp, pointer, and static segments.
    if segment == "static":
        s.append("@SP") # pop value into D
        s.append("AM=M-1")
        s.append("D=M")
        s.append("@" + str(index)) ## check this to be sure
        s.append("M=D")

    elif segment == "this":
        s.append("@" + str(index)) # get address into R13
        s.append("D=A")
        s.append("@THIS")
        s.append("D=M+D") 
        s.append("@R13")
        s.append( "M=D")
        s.append("@SP") # pop value into D
        s.append("AM=M-1")
        s.append( "D=M")
        s.append("@R13") # address back in A (not D)
        s.append("A=M")
        s.append("M=D")

    elif segment == "that":
        s.append("@" + str(index)) # get address into R13
        s.append("D=A")
        s.append("@THAT")
        s.append("D=M+D")
        s.append("@R13")
        s.append("M=D")
        s.append("@SP") # pop value into D
        s.append("AM=M-1")
        s.append("D=M")
        s.append("@R13") # address back in A (not D)
        s.append("A=M")
        s.append("M=D")

    elif segment == "argument":
        s.append("@" + str(index)) # get address into R13
        s.append("D=A")
        s.append("@ARG")
        s.append("D=M+D") 
        s.append( "@R13")
        s.append("M=D")
        s.append("@SP")# pop value into D
        s.append("AM=M-1")
        s.append("D=M")
        s.append("@R13") # address back in A (not D)
        s.append("A=M")
        s.append("M=D")

    elif segment == "local":
        s.append("@" + str(index)) # get address into R13
        s.append("D=A")
        s.append("@LCL")
        s.append("D=M+D") 
        s.append("@R13")
        s.append("M=D")
        s.append("@SP") #pop value into D
        s.append("AM=M-1")
        s.append("D=M")
        s.append("@R13") #address back in A (not D)
        s.append("A=M")
        s.append("M=D")

    elif segment == "pointer":
        s.append("@" + index) # get address into R13
        s.append("D=A")
        s.append("@3")
        s.append("D=A+D") 
        s.append("@R13")
        s.append("M=D")
        s.append("@SP") # pop value into D
        s.append("AM=M-1")
        s.append("D=M")
        s.append("@R13") # address back in A (not D)
        s.append("A=M")
        s.append("M=D")

    elif segment == "temp":
        s.append("@" + str(index)) # get address into R13
        s.append("D=A")
        s.append("@5")
        s.append("D=A+D") 
        s.append("@R13")
        s.append("M=D")
        s.append("@SP") # pop value into D
        s.append("AM=M-1")
        s.append("D=M")
        s.append("@R13") # address back in A (not D)
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

    if operation == "add":
      s.append("@SP") # pop first value into D
      s.append("AM=M-1")
      s.append("D=M") 
      s.append("@SP") # pop second value into M
      s.append("AM=M-1") 
      s.append("M=D+M") # push sum onto M
      s.append("@SP")
      s.append("M=M+1")    

    elif operation == "sub":
      s.append("@SP") # pop first value into D
      s.append("AM=M-1")
      s.append("D=M") 
      s.append("@SP") # pop second value into M
      s.append("AM=M-1") 
      s.append("M=M-D") # push difference onto M
      s.append("@SP")
      s.append("M=M+1")

    elif operation == "or":
      s.append("@SP") # pop first value into D
      s.append("AM=M-1")
      s.append("D=M") 
      s.append("@SP") # get second value into M
      s.append("A=M-1")
      s.append("M=D|M")
    
    elif operation == "and":
      s.append("@SP") # pop first value into D
      s.append("AM=M-1")
      s.append("D=M") 
      s.append("@SP") # get second value into M
      s.append("A=M-1")
      s.append("M=D&M") # put result back on stack

    else:
        print("Error Message") ##Error Message
    # FIXME: complete implementation for + , - , | , and & operators
    return s


def generate_unary_operation_code(operation):
    """Generate assembly code to perform the specified unary operation. 
    The operand is popped from the stack and the result of the operation 
    placed back in the stack.
    """
    s = []
    if operation == "neg":
      s.append("@SP") # get (not pop) value into M
      s.append("A=M-1") 
      s.append("M=-M") # and negate it

    elif operation == "not":
      s.append("@SP") # get (not pop) value into M
      s.append("A=M-1") 
      s.append("M=!M") # and negate it

    else:
        print("Error message")
    # FIXME: complete implementation for bit-wise not (!) and negation (-) operatiors
    
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
    s.append('A=M')
    s.append('D=M')             # D  = operand2
    s.append('@SP')
    s.append('M=M-1')           # Adjust stack pointer
    s.append('A=M')
    
    if operation=='eq':
        pass

    elif operation == 'lt':
        s.append('D=M-D')       # D = operand1 - operand2
        label_1 = 'IF_LT_' + str(line_number)
        s.append('@' + label_1)
        s.append('D;JLT')       # if operand1 < operand2 goto IF_LT_*
        s.append('@SP')
        s.append('A=M')
        s.append('M=0')          # Save result on stack 
        label_2 = 'END_IF_ELSE_' + str(line_number)
        s.append('@' + label_2)
        s.append('0;JMP')
        s.append('(' + label_1 + ')')
        s.append('@SP')
        s.append('A=M')
        s.append('M=-1')        # Save result on stack
        s.append('(' + label_2 + ')')

    elif operation =='gt':
        pass
   
    # FIXME: complete implementation for eq and gt operations
    
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
    
    # FIXME: complete implementation
    
    return s


def generate_goto_code(label):
    """Generate assembly code for goto."""
    s = []
    
    # TODO: complete implementation 
    
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

print(generate_set_code('lcl', '300'))




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