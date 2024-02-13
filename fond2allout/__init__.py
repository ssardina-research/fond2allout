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
import os
from fond2allout.translate import main as translate_main
from fond2allout.pddl.domprob import domprob_to_string

__version__: str = "1.0.0"



def translate(file_pddl, console, suffix, save):
    """Translate to all-outcome determinzation."""
    if save is None:
        base_name, _ = os.path.splitext(os.path.basename(file_pddl))
        save = f"{base_name}-allout.pddl"

    allout_domain, fond_domain = translate_main(file_pddl, suffix, save)

    if console:
        print(domprob_to_string((allout_domain, fond_domain)))
