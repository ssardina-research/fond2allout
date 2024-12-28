#! /usr/bin/env python3
import argparse
import itertools
import os

from pddl.logic.base import And, OneOf
from pddl.logic.predicates import Predicate
from pddl.core import Domain, Action, Problem
from pddl.formatter import domain_to_string, problem_to_string
from pddl.requirements import Requirements

from fond2allout.pddl import parse_domain_problem


def translate(fond_domain: Domain, suffix="DETDUP") -> Domain:
    """
    Compute the all-outcomes determinization of a FOND Domain
    Output is a new Domain but deterministic, with each ND action replaced by a set of deterministic actions with suffix _key_N, one for each possible outcome.
    """
    new_actions = []
    for act in fond_domain.actions:
        # collect all oneof effect of act in a list of lists oneof_effects
        # an action should start with an And (which may have OneOf blocks) or directly with a single OneOf
        if isinstance(act.effect, And):
            operands = act.effect.operands
        elif isinstance(act.effect, OneOf):
            operands = [act.effect]
        elif isinstance(act.effect, Predicate):
            operands = [act.effect]
        else:
            print(
                "Found an action effect that is not an AND or a OneOf. Type of effect:",
                type(act.effect),
            )
            print(act.effect)
            exit(1)
        det_effects = []
        oneof_effects = []
        nd_action = False
        for e in operands:
            if not isinstance(e, OneOf):
                det_effects.append(e)
                continue
            nd_action = True
            oneof_effects.append(list(e.operands))

        # build deterministic actions for act
        if nd_action:
            for i, one_effect in enumerate(list(itertools.product(*oneof_effects))):
                new_effect = det_effects + list(one_effect)
                a = Action(
                    f"{act.name}_{suffix}_{i}",
                    parameters=act.parameters,
                    precondition=act.precondition,
                    effect=And(*new_effect),
                )
                new_actions.append(a)
        else:
            new_actions.append(act)

    allout_domain = Domain(
        f"{fond_domain.name}_ALLOUT",
        requirements=frozenset(
            [
                r
                for r in fond_domain.requirements
                if r is not Requirements.NON_DETERMINISTIC
            ]
        ),
        types=fond_domain.types,
        constants=fond_domain.constants,
        predicates=fond_domain.predicates,
        actions=new_actions,
    )

    return allout_domain


def main(file: str, suffix="DETDUP", file_out=None) -> Domain:
    result: (Domain, Problem) = parse_domain_problem(file)

    fond_domain, fond_problem = result

    allout_domain = translate(fond_domain, suffix=suffix)

    if file_out:
        with open(file_out, "w") as f:
            f.write(domain_to_string(allout_domain))
            if fond_problem is not None:
                f.write("\n")
                f.write(problem_to_string(fond_problem))

    return allout_domain, fond_problem
