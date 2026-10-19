# Program Analysis for Software Security — Viper

Solutions and notes for the **Program Analysis for Software Security** course (Master in Cybersecurity). The course covers **automated program verification** using the [Viper](https://viper.ethz.ch/) verification infrastructure.

> *"Program testing can be used to show the presence of bugs, but never to show their absence!"*
> — Edsger W. Dijkstra

## Why program verification?

Testing checks a program on the inputs you *chose*. Verification proves it correct for *all* inputs. That matters for security: bugs such as the integer overflow in Java's binary search went unnoticed for about nine years despite testing.

Viper lets you annotate code with a specification. An SMT solver (Z3) then automatically proves that the code meets it.

```
source code + specification  ──►  verifier  ──►  ✓ verified   or   ✗ counterexample
```

## Repository structure

```
.
├── README.md
└── seminar1/
    └── seminar1.vpr     # Assignment 1: contracts, forward & backward reasoning
```

New seminars will be added as separate folders.

## Setup

1. Install **Java 11+** (64-bit), then set `JAVA_HOME` and add Java to your `PATH`.
2. Install **Visual Studio Code** (64-bit).
3. In VS Code, open the Extensions view (`Ctrl+Shift+X` / `⌘+Shift+X`), search for **Viper**, install it, and restart.
4. Open any `.vpr` file. It is verified automatically on save.
5. To switch the backend between **Silicon** and **Carbon**, click the backend name in the bottom-left status bar. Assignments should verify on both.

A successful run shows `Successfully verified <file>.vpr` in the status bar.

## Key concepts

### Contracts

A method contract consists of a precondition, a postcondition, and the method's signature.

```viper
method triple(x: Int) returns (r: Int)
    requires x % 2 == 0      // precondition: what the caller must guarantee
    ensures  r == 3 * x      // postcondition: what the method guarantees
{
    r := x / 2
    r := 6 * r
}
```

- **Modular verification:** at a call site, Viper uses only the callee's contract, never its body. If the contract is too weak, the caller cannot prove anything about the result.
- **Abstract methods:** a method with a contract but no body is *trusted*, not checked. An unsatisfiable contract, such as `ensures false`, makes everything after the call provable. This is the **trusted code base** problem.
- **`assert` vs `assume`:** `assert R` is checked. `assume R` is trusted without proof, and `assume false` makes anything verify.

### Floyd-Hoare triples

`{ Pre } S { Post }` is valid if every execution of `S` that starts in a state satisfying `Pre` terminates, without error, in a state satisfying `Post`.

### Forward reasoning: strongest postcondition (SP)

Start from `Pre` and move **down** the program, tracking exactly what is true. The SP is the most precise description of all reachable final states. To verify, check that `SP(Pre, S) ==> Post`.

### Backward reasoning: weakest precondition (WP)

Start from `Post` and move **up** the program, asking what must have been true before each statement. The WP is the least restrictive set of start states that guarantees `Post`. To verify, check that `Pre ==> WP(S, Post)`.

| Statement   | SP(P, S)                                    | WP(S, Q)                    |
|-------------|---------------------------------------------|-----------------------------|
| `x := a`    | `exists x0 :: P[x/x0] && x == a[x/x0]`      | `Q[x/a]`                    |
| `assert R`  | `P && R`                                    | `R && Q`                    |
| `assume R`  | `P && R`                                    | `R ==> Q`                   |
| `var x`     | `exists x :: P`                             | `forall x :: Q`             |
| `S1; S2`    | `SP(SP(P, S1), S2)`                         | `WP(S1, WP(S2, Q))`         |
| `S1 [] S2`  | `SP(P, S1) \|\| SP(P, S2)`                  | `WP(S1, Q) && WP(S2, Q)`    |

An `if (b) { S1 } else { S2 }` is encoded as `(assume b; S1) [] (assume !b; S2)`, so:

```
WP(if b then S1 else S2, Q) = (b ==> WP(S1, Q)) && (!b ==> WP(S2, Q))
```

**Example**

```
WP:  x > 3          // substitute 2 * x for y:  2 * x > 6
     y := 2 * x
     { y > 6 }
```

## Resources

- [Viper tutorial: Introduction](https://viper.ethz.ch/tutorial/#introduction)
- [Viper tutorial: Language overview](https://viper.ethz.ch/tutorial/#language-overview)
- [Viper project website](https://viper.ethz.ch/)

## Acknowledgements

Course material is based in part on slides by Peter Müller (ETH Zürich) and Christoph Matheja (DTU). Viper is developed by the Programming Methodology Group at ETH Zürich.