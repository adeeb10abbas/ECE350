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


def remove_whitespace(command):
    return "".join(command.split())

def char_is_valid(char): #TODO: Rewrite
    valid = False
    if char.isnumeric() or char.isalpha() or char == "@" or char == "=" or char == "(" or char == ")" \
            or char == "-" or char == "+" or char == ";"\
            or char == "_" or char == "." or char == "$" or char == ":":
        valid = True

    return valid


def A_register_symbol_isvalid(A_register_command):
    valid = False
    accepted_characters = ["_", ".", "$", ":"]
    if A_register_command[0].isalpha(): #first character after @ is a upper or lowercase letter
        for i in A_register_command:
            if i in accepted_characters or i.isalnum():
                valid = True

    elif A_register_command[0].isnumeric():
        if A_register_command.isnumeric(): #TODO: What is an accepted A-value command?
            valid = True

    return valid

def A_register_symbol_type(A_register_command):
    t =""
    if A_register_command.isnumeric():
        t = "NUMBER"
    else:
        t = "SYMBOL"

    return t


def validate_statement(command, rom_counter):
    command = remove_whitespace(command)

    s = {}
    s['instruction_type'] = ''
    s['value'] = ''
    s['value_type'] = ''
    s['dest'] = ''
    s['comp'] = ''
    s['jmp'] = ''
    s['status'] = -1 #error by default


    # A-type instructions
    if command[0] == "@":
        A_register_symbol = command[1:] #TODO: Check if symbol is user defined or not in second cycle. Anything goes for this parse.
        if A_register_symbol_isvalid(A_register_symbol):
            s["instruction_type"] = 'A-INSTRUCTION'
            s["value"] = A_register_symbol
            s["value_type"] = A_register_symbol_type(A_register_symbol)
            if s["value_type"] == "NUMBER":
                s['dest'] = 'null'
                s['jmp'] = 'null'
            s['status'] = 0

    #Labels
    elif "(" == command[0] and ")" == command[-1]:
        label = command[1:-1]
        print("Label: ", label)
        #print("A type label symbol:", symbol)
        if label not in symbol_table: #Add user defined label to symbol table
            symbol_table.update({f"{label}": rom_counter})
            s["instruction_type"] = 'LABEL'
            s['status'] = 0


    # C-type instructions
    elif "=" in command or ";" in command:
        dest = ''
        comp = ''
        jump = 'null'
        status = -1 #-1 by default; todo: can define up there too

        if "=" in command and ";" in command:
            lhs = command.split("=")

            p_dest = lhs[0]
            p_comp = lhs[1].split(";")[0]
            p_jump = command.split(";")[1]
            #print("dest: ", dest, "comp : ",comp, "jump",  jump)

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
            #print("only ; in command: ")
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

    else:
        s['status'] = -1

    print("Printing s:", s)
    return s


def parse(command):
    """Implements finite automate to scan assembly statements and parse them.

    WHITE SPACE: Space characters are ignored. Empty lines are ignored.

    COMMENT: Text beginning with two slashes (//) and ending at the end of the line is considered
    comment and is ignored.

    CONSTANTS: Must be non-negative and are written in decimal notation.

    SYMBOL: A user-defined symbol can be any sequence of letters, digits, underscore (_), dot (.),
    dollar sign ($), and colon (:) that does not begin with a digit.

    LABEL: (SYMBOL)

    1) Implement data structure to include all commands for second run
    2) Create a symbol table as you come across symbols. <me>What to do with labels though?

    """

    parsed_program = []
    rom_counter = 0
    f = open("assembler/series_sum.asm", "r")

    # Data structure to hold the parsed fields for the command

    line_counter = 0 #TODO: Remove; for testing purposes only
    for line in f.readlines():
        s = {}
        state = 0
        command = ''

        #checking for invalid characters and comments
        for char in line:
            if state == -1:
                state = -1  #Error state.
                print("Unrecognized character. Breaking now. ")
                break
            elif state == 0:
                if char == ' ':
                    state = 0  # Ignore blank spaces
                elif char == '\n':
                    state = 0  #Ignore blank lines??
                elif char == '/':
                    state = 1

                #couple elifs here and create token??
                elif char_is_valid(char):
                    command += char
                else:
                    state = -1  #Not a comment so fuck off

            elif state == 1:
                if char == '/':
                    state = 2
                else:
                    state = -1

            elif state == 2:
                state = 2
                break

            else:
                state = -1

        if state == -1: #TODO: How to handle outer loop- EXIT PROGRAM
            break #we want the outer loop to exit too if we encounter an unrecognized character

        else:
            if line_counter == 7: #TODO: Remove line counter
                # print(command)
                command_dict = validate_statement(command, rom_counter) #Validate command
                # print(command_dict)
                if command_dict["status"] == 0:
                    if command_dict["instruction_type"] == "A-INSTRUCTION" or \
                            command_dict["instruction_type"] == "C-INSTRUCTION":
                        rom_counter += 1
                        parsed_program.append(command_dict)

                else:
                    print("Invalid command")
                    break

        line_counter += 1


parse("Meaningless")

# validate_statement("(ece", 0)




"""
    @i
    M = 1       // i = 1
    @sum
    M = 0       // sum = 0

(LOOP)
    @i
    D = M       // D = i
    @10
    D = D - A   // D = i - 100
    @END
    D;JGT       // if (i - 100) > 0 goto END
    @i
    D = M       // D = i
    @sum
    M = M + D   // sum = sum + i
    @i 
    M = M + 1   // i = i + 1
    @LOOP
    0;JMP       // goto LOOP
"""