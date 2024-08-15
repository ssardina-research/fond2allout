#! /usr/bin/env python3
import argparse
import os

from fond2allout import translate


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate lifted all-outcomes determinization of a FOND planning domain"
    )
    parser.add_argument(
        "domain", nargs="?", help="(non-deterministic) PDDL domain file to determinize."
    )
    parser.add_argument("--save", type=str, help="file to save determinized model")
    parser.add_argument(
        "--suffix",
        type=str,
        default="DETDUP",
        help="suffix to use to annotate each deterministic version of an nd-action (Default: %(default)s)",
    )
    parser.add_argument(
        "--console",
        action="store_true",
        default=False,
        help="dump encoding to terminal too (Default: %(default)s)",
    )
    args = parser.parse_args()

    base_name, _ = os.path.splitext(os.path.basename(args.domain))
    out_pddl_file = f"{base_name}-allout.pddl"
    if args.save:
        out_pddl_file = args.save

    translate(os.path.abspath(args.domain), args.console, args.suffix, out_pddl_file)
