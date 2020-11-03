from format_asm_file import char_is_valid

def A_register_symbol_type(A_register_command):
    t =""
    if A_register_command.isnumeric():
        t = "NUMBER"
    else:
        t = "SYMBOL"

    return t


"""
A instruction

Input-contract: Any string that starts with @
Output-contract: in dictss,  s['status'] == 0 if valid A instruction symbol,
s['status'] = -1 otherwise 
"""

#TODO: Make sure function works against all the rules defined in the Hack specification.
def A_register_symbol_isvalid(possible_A_instruction):
    s = {}
    s["instruction_type"] = ''
    s["value"] = possible_A_instruction
    s["value_type"] = ""
    s['dest'] = ''
    s['jmp'] = ''
    s['status'] = -1


    possible_A_instruction = possible_A_instruction[1:] #Remove @
    valid = False
    accepted_characters = ["_", ".", "$", ":"]

    if possible_A_instruction[0].isalpha(): #first character after @ is a upper or lowercase letter
        for i in possible_A_instruction:
            if i in accepted_characters or i.isalnum():
                valid = True

    elif possible_A_instruction[0].isnumeric():
        if possible_A_instruction.isnumeric() and possible_A_instruction>0: #TODO: What is an accepted A-value command?
            valid = True

    if valid:
        s["instruction_type"] = 'A-INSTRUCTION'
        s["value"] = possible_A_instruction
        s["value_type"] = A_register_symbol_type(possible_A_instruction)
        if s["value_type"] == "NUMBER":
            s['dest'] = 'null'
            s['jmp'] = 'null'
        s['status'] = 0

    return s

"""
Labels

Input-contract: Any string that starts with (
Output-contract: If valid label, dict s with status = 0 
If invalid, dict s with status = -1
"""
#TODO: Make sure function works against all the rules defined in the Hack specification.
def label_isvalid(possible_label):
    s = {}
    s["instruction_type"] = ''
    s["value"] = possible_label
    s["value_type"] = ""
    s['dest'] = ''
    s['jmp'] = ''
    s['status'] = -1

    valid = False
    label = ''
    if "(" == possible_label[0] and ")" == possible_label[-1]:
        accepted_characters = ["_", ".", "$", ":"]
        label = possible_label[1:-1]
        #print("Label:", label)

        if label[0].isalpha():
            for i in label:
                if i in accepted_characters or i.isalnum():
                    valid = True
                else:
                    valid = False
                    break #Function exits if this happens with -1

        elif label[0].isnumeric():
            if label.isnumeric():
                valid = True

    if valid:
        s["instruction_type"] = 'LABEL'
        s["value"] = label
        s["value_type"] = 'SYMBOL'
        s['dest'] = ''
        s['jmp'] = ''
        s['status'] = 0

    #print(s)
    return s


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

valid_dest_patterns = {'null':'000',
                       'M':'001',
                       'D':'010',
                       'MD':'011',
                       'A':'100',
                       'AM':'101',
                       'AD':'110',
                       'AMD':'111'
                       }

valid_jmp_patterns =  {'null':'000',
                       'JGT':'001',
                       'JEQ':'010',
                       'JGE':'011',
                       'JLT':'100',
                       'JNE':'101',
                       'JLE':'110',
                       'JMP':'111'
                       }

"""
C instruction

Input-contract: A string with = or ; in it with all whitespace removed 
Output-contract: If valid C instruction, dict s with status = 0 and dest, comp and jmp values set
    If invalid, dict s with status = -1
"""

#TODO: Make sure function works against all the rules defined in the Hack specification.
def C_instruction_isvalid(command):
    s = {}
    s['instruction_type'] = ''
    s['value'] = ''
    s['value_type'] = ''
    s['dest'] = ''
    s['comp'] = ''
    s['jmp'] = 'null'
    s['status'] = -1  # error by default

    dest = ''
    comp = ''
    jump = 'null'
    status = -1  # -1 by default;

    if "=" in command and ";" in command:
        lhs = command.split("=")

        p_dest = lhs[0]
        p_comp = lhs[1].split(";")[0]
        p_jump = command.split(";")[1]
        # print("dest: ", dest, "comp : ",comp, "jump",  jump)

        if p_dest in valid_dest_patterns and p_comp in valid_comp_patterns \
                and p_jump in valid_jmp_patterns:
            dest = p_dest
            comp = p_comp
            jump = p_jump
            status = 0

    elif "=" in command:
        lhs = command.split("=")[0]
        rhs = command.split("=")[1]
        if lhs in valid_dest_patterns and rhs in valid_comp_patterns:
            dest = lhs
            comp = rhs
            status = 0

    elif ";" in command:
        # print("only ; in command: ")
        lhs = command.split(";")[0]
        rhs = command.split(";")[1]
        if lhs in valid_comp_patterns and rhs in valid_jmp_patterns:
            comp = lhs
            status = 0
        jump = rhs

    s['instruction_type'] = 'C-INSTRUCTION'
    s['dest'] = dest
    s['comp'] = comp
    s['jmp'] = jump
    s['status'] = status

    #print(s)
    return s

def validate_instruction(command):
    s = {}
    s['instruction_type'] = ''
    s['value'] = ''
    s['value_type'] = ''
    s['dest'] = ''
    s['comp'] = ''
    s['jmp'] = ''
    s['status'] = -1  #error by default

    try:
        #A type instructions
        if command[0] == "@":
            s = A_register_symbol_isvalid(command) #TODO: Returns valid S instruction dictionary

        #Labels
        elif command[0] == "(":
            s = label_isvalid(command)

        #C type instructions
        elif "=" in command or ";" in command:
            s = C_instruction_isvalid(command)

        else:
            return s #or something else


    except IndexError:
        return s

    return s



s = validate_instruction("(LOOP)")
print(s)






