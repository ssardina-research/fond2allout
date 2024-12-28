#
# Copyright 2021-2023 WhiteMech
#
# ------------------------------
#
# This file is part of pddl.
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
#

_all__ = ['pddl']

"""Top-level package for extending pddl parser to APP."""

def parse_domain_problem(fn):
    """This function parses a domain and/or problem PDDL file."""
    from fond2allout.pddl.domprob import DomProbParser

    with open(fn, "r") as f:
        ptext = f.read()
    return DomProbParser()(ptext)