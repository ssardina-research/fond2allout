#! /usr/bin/env python3
import argparse
import itertools
import os

from pddl.logic.effects import AndEffect
from pddl.logic.base import And, OneOf
from pddl.logic.predicates import Predicate
from pddl import parse_domain
from pddl.core import Domain, Action
from pddl.formatter import domain_to_string


def _fond2allout(fond_domain: Domain, suffix="DETDUP") -> Domain:
    """
    Compute the all-outcomes determinization of a FOND Domain
    Output is a new Domain but deterministic, with each ND action replaced by a set of deterministic actions with suffix _key_N, one for each possible outcome.
    """
    new_actions = []
    for act in fond_domain.actions:
        # collect all oneof effect of act in a list of lists oneof_effects
        # an action should start with an AndEffect (which may have OneOf blocks) or directly with a single OneOf
        if isinstance(act.effect, AndEffect):
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
        requirements=frozenset([r for r in fond_domain.requirements if str(r) != ":non-deterministic"]),
        types=fond_domain.types,
        constants=fond_domain.constants,
        predicates=fond_domain.predicates,
        actions=new_actions,
    )

    return allout_domain



def main(fond_domain_file: str, suffix="DETDUP", file_out=None) -> Domain:
    fond_domain: Domain = parse_domain(fond_domain_file)

    allout_domain = _fond2allout(fond_domain, suffix=suffix)

    if file_out:
        with open(file_out, "w") as f:
            f.write(domain_to_string(allout_domain))

    return allout_domain


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate lifted all-outcomes determinization of a FOND domain"
    )
    parser.add_argument("domain", nargs="?", help="domain PDDL file to determinize.")
    parser.add_argument("--save", type=str, help="file to save determinized model")
    parser.add_argument(
        "--suffix",
        type=str,
        default="DETDUP",
        help="suffix to use to annotate each deterministic version of an nd-action (Default: %(default)s)",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        default=False,
        help="dump encoding to terminal too (Default: %(default)s)",
    )
    args = parser.parse_args()

    base_name, _ = os.path.splitext(os.path.basename(args.domain))
    out_pddl_file = f"{base_name}-allout.pddl"
    if args.save:
        out_pddl_file = args.save

    allout_domain = main(os.path.abspath(args.domain), suffix=args.suffix, file_out=out_pddl_file)

    if args.print:
        print(domain_to_string(allout_domain))
