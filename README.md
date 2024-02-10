# FOND All-outcome Lifted Determinizers

This repo contains a script to determinize a PDDL FOND planning domain with `oneof` clauses.

In the _all-outcome determinization_, each non-deterministic action is replaced with a set of deterministic actions, each encoding one possible effect outcome of the action. A solution in the deterministic version amounts to a weak plan solution in the original FOND problem.

Note this determinizer produces another PDDL FOND domain and does not deal with the problem itself, unlike the SAS-based determinizers used in other planners like [PRP](https://github.com/QuMuLab/planner-for-relevant-policies), [FONDSAT](https://github.com/tomsons22/FOND-SAT), or [CFOND-ASP](https://github.com/ssardina-research/cfond-asp) that produces a SAS encoding of the determinization of a specific instance planning problem and are based on the SAS translator in [Fast-Downard](https://github.com/aibasel/downward) classical planner.

# Pre-requisites

The script relies on the [pddl](https://github.com/AI-Planning/pddl) parser, which can be easily installed via:

```shell
$ pip install pddl
```

The pddl system relies itself on the [lark](https://lark-parser.readthedocs.io/en/stable/) parsing library.

# Example runs

A simple example run is as follows:

```shell
$ python fond2allout.py problems/blocksworld-ipc08/domain.pddl
```

This will save the all-outcome deterministic PDDL version in file `domain-allout.pddl`. Deterministic versions of non-deterministic actions will be indexed with term `_DETDUP_<n>`, as done by [PRP](https://github.com/QuMuLab/planner-for-relevant-policies)'s original determinizer. The name of the determinized domain will be the original name with suffix `_ALLOUT`.

To change the suffix use option `--suffix`, to change the output file use `--save`, and to get the resulting PDDL printed on console use `--print`:

```lisp
$ python fond2allout.py problems/blocksworld-ipc08/domain.pddl --print --suffix "VER" --save output.pddl                                                                    ─╯
(define (domain blocks-domain_ALLOUT)
    (:requirements :equality :typing)
    (:types block)
    (:predicates (clear ?b - block)  (emptyhand) (holding ?b - block)  (on ?b1 - block ?b2 - block)  (on-table ?b - block))
    (:action pick-tower
        :parameters (?b1 - block ?b2 - block ?b3 - block)
        :precondition (and (emptyhand) (on ?b1 ?b2) (on ?b2 ?b3))
        :effect (and (holding ?b2) (clear ?b3) (not (emptyhand)) (not (on ?b2 ?b3)))
    )
     (:action pick-up-from-table
        :parameters (?b - block)
        :precondition (and (emptyhand) (clear ?b) (on-table ?b))
        :effect (and (holding ?b) (not (emptyhand)) (not (on-table ?b)))
    )
     (:action pick-up_VER_0
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (holding ?b1) (clear ?b2) (not (emptyhand)) (not (clear ?b1)) (not (on ?b1 ?b2)))
    )
     (:action pick-up_VER_1
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (clear ?b2) (on-table ?b1) (not (on ?b1 ?b2)))
    )
     (:action put-down
        :parameters (?b - block)
        :precondition (holding ?b)
        :effect (and (on-table ?b) (emptyhand) (clear ?b) (not (holding ?b)))
    )
...
```

Note this resulting PDDL domain is now deterministic and can then be used as input to the original [Fast-Downard](https://github.com/aibasel/downward) SAS translator.

## Format allowed on effects

The determinizer accepts effects that are a single top-level `oneof` clause or mentioned as clauses in the top-level `And` effect. As such, `oneof` should not be mentioned inside other `oneof` clauses or internal `and` clauses.

If the effect is just one `oneof` clause, then it corresponds to the Unary Nondeterminism (1ND) Normal Form without conditionals in:

* Jussi Rintanen: [Expressive Equivalence of Formalisms for Planning with Sensing](https://gki.informatik.uni-freiburg.de/papers/Rintanen03expr.pdf). ICAPS 2003: 185-194

However, the translator is able to handle more flexible formats, like:

- Single predicate effect, like `:effect (door_unlocked ?r)`
- Single oneof effect, like `:effect (oneof (and (on-table ?b) (emptyhand)) (and (on ?b ?c) (emptyhand)))`
- And-effect with many `oneof` clauses, like
    `:effect (and (f1) (f2) (oneof ......) (f3) (oneof .....) (f4) (oneof ....))`

When there are many `oneof` clauses in a top-level `and` effect, the cross-product of all the `oneof` clauses will determine the deterministic actions.




