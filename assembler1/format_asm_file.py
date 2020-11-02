"""Formatting:
1. Remove new line
2. Remove spaces between files and all redundant whitespace
"""

def char_is_valid(char): #TODO: Rewrite
    valid = False
    if char.isnumeric() or char.isalpha() or char == "@" or char == "=" or char == "(" or char == ")" \
            or char == "-" or char == "+" or char == ";"\
            or char == "_" or char == "." or char == "$" or char == ":":
        valid = True

    return valid


"""
Input contract: Any line
Output Contract: If line does not have asm comments, return it as it is 
If line has comments, remove comments and return line 
If line is a comment, return -2
If line is invalid return -1

"""
def remove_comments(line):
    state = 0
    command = ''

    for char in line:
        if state == -1:
            state = -1
            break

        elif state == 0:
            if char == " ":
                state = 0
            elif char == "\n":
                state = 0
            elif char == "/":
                state = 1

            elif char_is_valid(char):
                command += char

            else:
                state = -1

        elif state == 1:
            if char == "/":
                state = 2
            else:
                state = -1

        elif state == 2:

            state = 2

    if state == -1:
        #print("Invalid input", -1)
        return -1

    elif command:
        #print(command)
        return command #cleaned command

    else:
        #print("This line is a comment", -2)
        return -2

def format_asm_file(filename):
    formatted_list1 = {}
    line_counter = 1

    f = open(filename, "r")
    for line in f.readlines():
        if line == "\n": #how do we get the line number if we're removing new lines?
            line_counter += 1
            continue

        else:
            line = line.replace(" ", "")
            formatted_list1.update({line_counter:line}) #{"line_number": line_content}
            line_counter += 1


    #print("Formatted list 1: ", formatted_list1) #deleted whitespaces and new line characters


    error = False
    error_line = 0
    formatted_list2 = {"status": 0, "error_line": error_line} #elements with comments removed
    for i in formatted_list1.keys():
        elem = remove_comments(formatted_list1[i])
        #print("first elem", elem)

        if elem == -2:
            continue #line is a comment, don't add to formatted list 2- go to next line

        elif elem == -1: #error- invalid character
            error = True
            error_line = i
            break

        else:
            formatted_list2.update({i : elem})

    if error:
        formatted_list2["status"] = -1
        formatted_list2["error_line"] = error_line

    return formatted_list2


format_asm_file("mult.asm")


"""
Test Inputs:
//hello hi 
@a //hi hello 
eiri=ien //hi hello 
/hi 
"""

remove_comments("hello hi  //hi ")