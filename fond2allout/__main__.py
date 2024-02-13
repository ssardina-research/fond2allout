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

"""Tool to check parsing of PDDL files."""
import os
import sys

import click

from fond2allout.pddl import parse_domain_problem
from fond2allout.pddl.domprob import domprob_to_string
from fond2allout.translate import main as translate_main
from pddl.formatter import domain_to_string
from fond2allout import translate as fond2allout_translate

@click.group()
def cli():
    """The unquestionable parser for PDDL 3.1."""  # noqa
quiet_option = click.option("-q", "--quiet", is_flag=True, help="Don't print anything.")

@cli.command()
@click.argument("file_pddl", type=click.Path(exists=True, dir_okay=False))
@quiet_option
def check(file_pddl, quiet):
    """Check a PDDL domain file is correct."""
    if quiet:
        sys.stdout = open(os.devnull, "a")
    print(domprob_to_string(parse_domain_problem(file_pddl)))


@cli.command()
@click.argument('file_pddl', type=click.Path(exists=True, dir_okay=False))
@click.option("--console", is_flag=True, help="Print the result on console")
@click.option('--suffix', type=str, default="DETDUP", help="suffix to use to annotate each deterministic version of an nd-action",)
@click.option('--save', type=str, default=None, help="file to save the determinized model")
def translate(file_pddl, console, suffix, save):
    """Translate to all-outcome determinzation."""
    if save is None:
        base_name, _ = os.path.splitext(os.path.basename(file_pddl))
        save = f"{base_name}-allout.pddl"

    fond2allout_translate(file_pddl, console, suffix, save)

if __name__ == "__main__":
    cli()
