@i
M=1
(LOOP)
@i
D=M
@R1
D=D-M
@END
D;JGT
@R0
D=M
@mul
M=M+D
@i
M=M+1
@LOOP
0;JMP
(END)
@END
0;JMP