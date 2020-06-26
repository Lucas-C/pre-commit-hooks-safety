from __future__ import print_function

import argparse
import sys

from safety.cli import check


def _parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--full-report",
        default="--full-report",
        const="--full-report",
        action="store_const",
    )
    parser.add_argument(
        "--short-report",
        dest="full_report",
        const="--short-report",
        action="store_const",
    )
    parser.add_argument("--ignore", "-i", action="append")
    parser.add_argument("files", nargs="+")
    return parser


def main(argv=None):
    parsed_args, rest = _parser().parse_known_args(argv)
    ignore = [
        arg
        for vs in parsed_args.ignore or []
        for code in vs.split(",")
        for arg in ("--ignore", code.strip())
    ]
    files = [arg for f in parsed_args.files for arg in ("--file", f)]
    args = [parsed_args.full_report] + ignore + files + rest
    try:
        check.main(args)
    except SystemExit as error:
        return error.code
    return 1


if __name__ == "__main__":
    sys.exit(main())
