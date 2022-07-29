"""Safety utilities."""
from __future__ import print_function


# Standar libraries
import argparse
import os
import sys
from contextlib import contextmanager
from shutil import which
from pathlib import Path
from subprocess import check_call
from tempfile import NamedTemporaryFile

#Third part libraries
from safety.cli import cli


def build_parser():
    """Build a parser in order to get args."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--full-report",
        dest="report_arg",
        action="store_const",
        const="--full-report",
        default="--full-report",
    )
    parser.add_argument(
        "--short-report",
        dest="report_arg",
        action="store_const",
        const="--short-report",
    )
    parser.add_argument("--ignore", "-i", action="append")
    parser.add_argument("files", nargs="+")
    return parser


def main(argv=None):  # pylint: disable=inconsistent-return-statements
    parser = build_parser()
    parsed_args, args_rest = parser.parse_known_args(argv)
    if all("requirements" in file_path for file_path in parsed_args.files):
        return call_safety_check(parsed_args.files, parsed_args.ignore, parsed_args.report_arg, args_rest)
    files = [Path(f) for f in parsed_args.files]
    if len(files) == 1 and files[0].name == "pyproject.toml":
        pyproject_toml_filepath = files[0]
        with pyproject_toml_filepath.open() as pyproject_file:
            lines = [line.strip() for line in pyproject_file.readlines()]
        if any(line.startswith("[tool.poetry]") for line in lines):
            with convert_poetry_to_requirements(pyproject_toml_filepath) as tmp_requirements:
                return call_safety_check([tmp_requirements.name], parsed_args.ignore, parsed_args.report_arg, args_rest)
        parser.error("Unsupported build tool: this pre-commit hook currently only handles pyproject.toml with Poetry"
                     " ([tool.poetry] must be present in pyproject.toml)")
    else:
        parser.error(f"Unsupported mix of pyproject.toml & requirements files found: {parsed_args.files}")


def call_safety_check(requirements_file_paths, ignore_args, report_arg, args_rest):
    """Call the safety cli checks."""
    safety_args = []
    if "--disable-telemetry" in args_rest:
        safety_args.append("--disable-telemetry")
        args_rest = [arg for arg in args_rest if arg != "--disable-telemetry"]
    safety_args.append("check")
    for file_path in requirements_file_paths:
        safety_args += ["--file", file_path]
    for codes in (ignore_args or []):
        for code in codes.split(","):
            safety_args += ["--ignore", code]
    try:
        cli.main(safety_args + [report_arg] + args_rest, prog_name="safety")
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
