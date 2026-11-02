#  How we model it:
#                 Left   Middle  Right
#      Alice      xal    xam     xar
#      Bob        xbl    xbm     xbr
#      Charlie    xcl    xcm     xcr
#
#  Logic rules used
#    Implies(A, B)  =  "if A then B"  =  Not(A) or B
#    Or(a, b, c)    =  at least one of a, b, c is true
#    at most one of a, b, c  =  no two of them are true at the same time
#    exactly one    =  at least one  AND  at most one
#
#  Meaning of the answer
#    sat   = there is an assignment making every constraint true (a valid seating)
#    unsat = no assignment satisfies all constraints (impossible to make all happy)
# =====================================================================

from z3 import *

# Declare the 9 Boolean variables from the table above.
# Bools("a b c") creates one Bool per name, in the same order.
xal, xam, xar, xbl, xbm, xbr, xcl, xcm, xcr = Bools(
    "xal xam xar xbl xbm xbr xcl xcm xcr"
)

s = Solver()

# ---------------------------------------------------------------------
# (1) Alice does not sit next to Charlie
# ---------------------------------------------------------------------
#   - Alice on Left  : her only neighbor is Middle  -> Charlie not on Middle
#   - Alice on Right : her only neighbor is Middle  -> Charlie not on Middle
#     Both cases have the same consequence, so we merge them with Or:
#       Implies(Or(xal, xar), Not(xcm))
#   - Alice on Middle: her neighbors are Left and Right -> Charlie on neither
#       Implies(xam, And(Not(xcl), Not(xcr)))
#   Both cases must hold, so we join them with And.
s.add(And(Implies(Or(xal, xar), Not(xcm)), Implies(xam, And(Not(xcl), Not(xcr)))))


# ---------------------------------------------------------------------
# (2) Alice does not sit on the leftmost chair
# ---------------------------------------------------------------------
s.add(Not(xal))


# ---------------------------------------------------------------------
# (3) Bob does not sit to the right of Charlie
# ---------------------------------------------------------------------
# Thinking: "to the right of" depends on where Charlie is, so we split on his chair.
#   - Charlie on Left  : Middle and Right are to his right -> Bob on neither
#       Implies(xcl, And(Not(xbm), Not(xbr)))
#   - Charlie on Middle: only Right is to his right        -> Bob not on Right
#       Implies(xcm, Not(xbr))
#   - Charlie on Right : nothing is to his right           -> no restriction,
s.add(And(Implies(xcl, And(Not(xbm), Not(xbr))), Implies(xcm, Not(xbr))))


# ---------------------------------------------------------------------
# (R1) Each person gets a chair  (at least one chair per person)
# ---------------------------------------------------------------------
# Thinking: without this, Z3 could set all of Alice's/ Bob's/ Charlie's variables to False,
s.add(Or(xal, xam, xar))  # Alice sits somewhere
s.add(Or(xbl, xbm, xbr))  # Bob sits somewhere
s.add(Or(xcl, xcm, xcr))  # Charlie sits somewhere


# ---------------------------------------------------------------------
# (R2) Every person gets at most one chair
# ---------------------------------------------------------------------
# Thinking: without this, Z3 could seat Alice on two chairs at once.
#   We forbid every pair of chairs in the same ROW of the table
#   (see "at most one" in the rules above):
#   - if Alice is on Left,   she is not on Middle and not on Right  -> pairs (L,M), (L,R)
#   - if Alice is on Middle, she is not on Right                    -> pair  (M,R)
#   Together with (R1) this means: every person sits on EXACTLY one chair.
s.add(And(Implies(xal, And(Not(xam), Not(xar))), Implies(xam, Not(xar))))  # Alice
s.add(And(Implies(xbl, And(Not(xbm), Not(xbr))), Implies(xbm, Not(xbr))))  # Bob
s.add(And(Implies(xcl, And(Not(xcm), Not(xcr))), Implies(xcm, Not(xcr))))  # Charlie


# ---------------------------------------------------------------------
# (R3) Every chair gets at most one person
# ---------------------------------------------------------------------
# Thinking: without this, two guests could share one chair.
#   Same "at most one" pattern as (R2), but now over a COLUMN of the table:
#   - if Alice is on this chair, Bob and Charlie are not
#   - if Bob is on this chair, Charlie is not
s.add(And(Implies(xal, And(Not(xbl), Not(xcl))), Implies(xbl, Not(xcl))))  # Left chair
s.add(
    And(Implies(xam, And(Not(xbm), Not(xcm))), Implies(xbm, Not(xcm)))
)  # Middle chair
s.add(And(Implies(xar, And(Not(xbr), Not(xcr))), Implies(xbr, Not(xcr))))  # Right chair


print(s.check())
