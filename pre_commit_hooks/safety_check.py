from __future__ import print_function

import argparse
import sys

from safety.cli import check


parser = argparse.ArgumentParser()
parser.add_argument(
    "--full-report",
    default="--full-report",
    const="--full-report",
    action="store_const",
)
parser.add_argument(
    "--short-report", dest="full_report", const="--short-report", action="store_const"
)
parser.add_argument("--ignore", action="append")
parser.add_argument("files", nargs="*", action="append")


def main(argv):
    ns, rest = parser.parse_known_args(["safety_check"] + args)
    ignore = [
        arg
        for vs in ns.ignore
        for code in vs.split(",")
        for arg in ("--ignore", arg)
    ]
    files = [arg for f in ns.files for arg in ("--file", f)]
    args = ([ns.full_report] + ignore + files + rest)
    try:
        check.main(args)
    except SystemExit as error:
        if error.code == 0:
            return 0
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
