; Exercise: Placement of wedding guests
; We have to assign chairs to three guests, called Alice, Bob, and Charlie
; There are three chairs in a row, called Left, Middle, and Right
; Alice does not want to sit on the leftmost chair
; Alice does not want to sit next to Charlie
; Bob does not want to sit to the right of Charlie
; Is it possible to assign our guests such that they are all happy?

; =====================================================================
;  Program Analysis for Software Security - Seminar 2 / Assignment 2
;  Same model as wedding.py, written in SMT-LIB (the input language of z3)
;  Run with:  z3 wedding.smt2
; =====================================================================
;
;  Reading SMT-LIB
;    Everything is in prefix form: the operator comes first, inside brackets.
;      (not A)          = not A
;      (and A B C)      = A and B and C
;      (or A B C)       = A or B or C
;      (=> A B)         = A implies B  = "if A then B"  = (not A) or B
;    So  (=> AM (and (not CL) (not CR)))  reads:
;        "if Alice is on Middle then (Charlie is not on Left and not on Right)"
;
;  Logic rules used (same as in wedding.py)
;    at least one of a, b, c  =  (or a b c)
;    at most one of a, b, c   =  no two of them are true at the same time
;    exactly one              =  at least one AND at most one
; =====================================================================
;
; Thinking: SAT only knows true/false, so we cannot write "Alice = Middle".
;   Instead we make one Bool per (person, chair) pair:
;
;                 Left   Middle  Right
;      Alice      AL     AM      AR
;      Bob        BL     BM      BR
;      Charlie    CL     CM      CR

(declare-const AL Bool)  
(declare-const AM Bool)  
(declare-const AR Bool)  
(declare-const BL Bool)  
(declare-const BM Bool)  
(declare-const BR Bool)  
(declare-const CL Bool)  
(declare-const CM Bool)  
(declare-const CR Bool)  

; ---------------------------------------------------------------------
; (2) Alice does not want to sit on the leftmost chair
; ---------------------------------------------------------------------
; Thinking: "Alice sits on Left" is exactly the variable AL,
;   so we require AL to be false.
(assert (not AL))

; ---------------------------------------------------------------------
; (1) Alice does not want to sit next to Charlie
; ---------------------------------------------------------------------
; Thinking: "next to" depends on where Alice is, so we split on her chair.
;   Neighbors: Left <-> Middle, Middle <-> Right  (Left and Right are NOT neighbors)
;   - Alice on Left or Right: her only neighbor is Middle
;       -> Charlie not on Middle
;   - Alice on Middle: her neighbors are Left and Right
;       -> Charlie on neither
;   Both cases must hold, so they are joined with and.
(assert
    (and
        (=> (or AL AR) (not CM))          
        (=> AM (and (not CL) (not CR))) 
    )
)

; ---------------------------------------------------------------------
; (3) Bob does not want to sit to the right of Charlie
; ---------------------------------------------------------------------
; Thinking: "to the right of" depends on where Charlie is, so we split on his chair.
;   - Charlie on Left  : Middle and Right are to his right -> Bob on neither
;   - Charlie on Middle: only Right is to his right        -> Bob not on Right
;   - Charlie on Right : nothing is to his right           -> no restriction needed
(assert
    (and
        (=> CL (and (not BM) (not BR)))   
        (=> CM (not BR))                   
    )
)

; ---------------------------------------------------------------------
; (R1) Each person gets a chair  (at least one chair per person)
; ---------------------------------------------------------------------
(assert
    (and
        (or AL AM AR)                      ; Alice sits somewhere
        (or BL BM BR)                      ; Bob sits somewhere
        (or CL CM CR)                      ; Charlie sits somewhere
    )
)

; ---------------------------------------------------------------------
; (R2) Every person gets at most one chair
; ---------------------------------------------------------------------
; Thinking: without this, z3 could seat one person on two chairs at once.
;   - if on Left, then not on Middle and not on Right   -> pairs (L,M), (L,R)
;   - if on Middle, then not on Right                   -> pair  (M,R)
(assert
    (and
        (and (=> AL (and (not AM) (not AR))) (=> AM (not AR)))   ; Alice
        (and (=> BL (and (not BM) (not BR))) (=> BM (not BR)))   ; Bob
        (and (=> CL (and (not CM) (not CR))) (=> CM (not CR)))   ; Charlie
    )
)

; ---------------------------------------------------------------------
; (R3) Every chair gets at most one person
; ---------------------------------------------------------------------
; Thinking: without this, two guests could share one chair.
;   - if Alice is on this chair, Bob and Charlie are not
;   - if Bob is on this chair, Charlie is not

(assert
    (and
        (and (=> AL (and (not BL) (not CL))) (=> BL (not CL)))   ; Left chair
        (and (=> AM (and (not BM) (not CM))) (=> BM (not CM)))   ; Middle chair
        (and (=> AR (and (not BR) (not CR))) (=> BR (not CR)))   ; Right chair
    )
)

(check-sat)
