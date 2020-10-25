@R2
 M = 0
 @R3
 M = 0
 @R0
 D = M
 @END
 D, JEQ
 @store
 M = D  // store to restore
(LOOP)
 @R1
 D = D - M
 @REMAINDER
 D, JLT
 @R2
 M = M + 1
 @EVENLY
 D, JEQ 
 @LOOP
 0, JMP
 
(REMAINDER)
 @R1
 D = D + M
 @R3
 M = D
(EVENLY)
 @store
 D = M
 @R0
 M = D
 
(END)
 @END
 0, JMP