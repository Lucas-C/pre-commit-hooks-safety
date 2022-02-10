from __future__ import print_function

import argparse
import os
import sys
from contextlib import contextmanager
from shutil import which
from pathlib import Path
from subprocess import check_call
from tempfile import NamedTemporaryFile

from safety.cli import check


def build_parser():
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


def main(argv=None):  # pylint: disable=inconsistent-return-statements
    parser = build_parser()
    parsed_args, args_rest = parser.parse_known_args(argv)
    if all("requirements" in file_path for file_path in parsed_args.files):
        return call_safety_check(parsed_args.files, parsed_args.ignore, parsed_args.full_report, args_rest)
    files = [Path(f) for f in parsed_args.files]
    if len(files) == 1 and files[0].name == "pyproject.toml":
        pyproject_toml_filepath = files[0]
        with pyproject_toml_filepath.open() as pyproject_file:
            lines = [line.strip() for line in pyproject_file.readlines()]
        if any(line.startswith("[tool.poetry]") for line in lines):
            with convert_poetry_to_requirements(pyproject_toml_filepath) as tmp_requirements:
                return call_safety_check([tmp_requirements.name], parsed_args.ignore, parsed_args.full_report, args_rest)
        parser.error("Unsupported build tool: this pre-commit hook currently only handles pyproject.toml with Poetry")
    else:
        parser.error("Unsupported mix of pyproject.toml & requirements files found")


def call_safety_check(requirements_file_paths, ignore_args, full_report_arg, args_rest):
    safety_args = []
    for file_path in requirements_file_paths:
        safety_args += ["--file", file_path]
    for codes in (ignore_args or []):
        for code in codes.split(","):
            safety_args += ["--ignore", code]
    try:
        check.main(safety_args + [full_report_arg] + args_rest, prog_name="safety")
    except SystemExit as error:
        return error.code
    return 1


@contextmanager
def convert_poetry_to_requirements(pyproject_toml_filepath):  # Sad function name :(
    poetry_cmd_path = which("poetry")
    if not poetry_cmd_path:  # Using install-poetry.py installation $PATH:
        poetry_cmd_path = os.path.join(os.environ.get("HOME", ""), ".local", "bin", "poetry")
        if not os.path.exists(poetry_cmd_path):  # Old get-poetry.py installation $PATH:
            poetry_cmd_path = os.path.join(os.environ.get("HOME", ""), ".poetry", "bin", "poetry")
    # Always passing delete=False to NamedTemporaryFile in order to avoid permission errors on Windows:
    try:
        ntf = NamedTemporaryFile(delete=False)
        with ntf:
            # Placing ourselves in the pyproject.toml parent directory:
            with chdir(pyproject_toml_filepath.parent):
                check_call([poetry_cmd_path, "export", "--dev", "--format", "requirements.txt", "--output", ntf.name])
            yield ntf
    finally:  # Manually deleting temporary file:
        os.remove(ntf.name)


@contextmanager
def chdir(path):
    """
    On enter, change directory to specified path.
    On exit, change directory to original.
    """
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


if __name__ == "__main__":
    sys.exit(main())
