from z3 import *
xal, xam, xar, xbl, xbm, xbr, xcl, xcm, xcr = Bools('xal xam xar xbl xbm xbr xcl xcm xcr')
s = Solver()

# Alice does not sit next to Charlie
s.add( And( Implies( Or(xal, xar), Not(xcm) ), Implies( xam, And( Not(xcl), Not(xcr)))))

# Alice does not sit on the leftmost chair
s.add( Not(xal) )

# Bob does not sit to the right of Charlie
s.add( And( Implies( xcl, And( Not(xbm), Not(xbr) ) ), Implies( xcm, Not(xbr) ) ) )

# Each person gets a chair
s.add( Or(xal, xam, xar) )
s.add( Or(xbl, xbm, xbr) )
s.add( Or(xcl, xcm, xcr) )

# Every person gets at most one chair
s.add( And( Implies( xal, And( Not(xam), Not(xar) ) ), Implies( xam, Not(xar) ) ) )
s.add( And( Implies( xbl, And( Not(xbm), Not(xbr) ) ), Implies( xbm, Not(xbr) ) ) )
s.add( And( Implies( xcl, And( Not(xcm), Not(xcr) ) ), Implies( xcm, Not(xcr) ) ) )

# Every chair gets at most one person
s.add( And( Implies( xal, And( Not(xbl), Not(xcl) ) ), Implies( xbl, Not(xcl) ) ) )
s.add( And( Implies( xam, And( Not(xbm), Not(xcm) ) ), Implies( xbm, Not(xcm) ) ) )
s.add( And( Implies( xar, And( Not(xbr), Not(xcr) ) ), Implies( xbr, Not(xcr) ) ) )

print( s.check() )
