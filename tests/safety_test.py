# pylint: disable=invalid-name,line-too-long
import pytest
from safety.constants import EXIT_CODE_VULNERABILITIES_FOUND

from pre_commit_hooks.safety_check import main as safety


def test_dev_requirements():
    assert safety(["dev-requirements.txt"]) == 0


def test_non_ok_dependency(tmp_path):
    requirements_file = tmp_path / "requirements.txt"
    with open(requirements_file, "w", encoding="utf-8") as file:
        file.write("urllib3==1.24.1")

    assert safety([str(requirements_file)]) == EXIT_CODE_VULNERABILITIES_FOUND


def test_short_report(tmp_path):
    requirements_file = tmp_path / "requirements.txt"
    with open(requirements_file, "w", encoding="utf-8") as file:
        file.write("urllib3==1.24.1")

    assert (
        safety(["--short-report", str(requirements_file)])
        == EXIT_CODE_VULNERABILITIES_FOUND
    )


def test_disable_telemetry(tmp_path):
    requirements_file = tmp_path / "requirements.txt"
    with open(requirements_file, "w", encoding="utf-8") as file:
        file.write("urllib3==1.24.1")

    assert (
        safety(["--disable-optional-telemetry-data", str(requirements_file)])
        == EXIT_CODE_VULNERABILITIES_FOUND
    )


@pytest.mark.parametrize("report", [["--full-report"], []])
def test_full_report(tmp_path, report, capfd):
    requirements_file = tmp_path / "requirements.txt"
    with open(requirements_file, "w", encoding="utf-8") as file:
        file.write("urllib3==1.24.1")

    assert safety(report + [str(requirements_file)]) == EXIT_CODE_VULNERABILITIES_FOUND
    output = capfd.readouterr().out
    assert "urllib3" in output
    assert "1.24.1" in output


@pytest.mark.parametrize(
    "args",
    [
        ["--ignore=37055,37071,38834,43975,61601,61893,71562,71608"],
        [
            "--ignore=37055",
            "--ignore=37071",
            "--ignore=38834",
            "--ignore=43975",
            "--ignore=61601",
            "--ignore=61893",
            "--ignore=71562",
            "--ignore=71608",
        ],
    ],
)
def test_ignore_ok(capfd, tmp_path, args):
    requirements_file = tmp_path / "requirements.txt"
    with open(requirements_file, "w", encoding="utf-8") as file:
        file.write("urllib3==1.24.1")

    assert safety([str(requirements_file)] + args) == 0, capfd.readouterr()


@pytest.mark.parametrize(
    "ignore_arg,status",
    [
        ("--ignore=37055,37071,38834,43975,61601,61893,71562,71608", 0),
        (
            "--ignore=37055,37071,38834,43975,61601,61893,71562",
            EXIT_CODE_VULNERABILITIES_FOUND,
        ),
        ("--ignore=37055", EXIT_CODE_VULNERABILITIES_FOUND),
        ("--ignore=37071", EXIT_CODE_VULNERABILITIES_FOUND),
        ("--ignore=38834", EXIT_CODE_VULNERABILITIES_FOUND),
    ],
)
def test_varargs_escape(tmp_path, ignore_arg, status):
    requirements_file = tmp_path / "requirements.txt"
    with open(requirements_file, "w", encoding="utf-8") as file:
        file.write("urllib3==1.24.1")

    assert safety([ignore_arg, "--", str(requirements_file)]) == status


def test_poetry_requirements(
    tmp_path,
):  # cf. https://github.com/Lucas-C/pre-commit-hooks-safety/issues/5
    requirements_file = tmp_path / "requirements.txt"
    with open(requirements_file, "w", encoding="utf-8") as file:
        file.write(
            """colored==1.4.2
colored-traceback==0.3.0 \
    --hash=sha256:6da7ce2b1da869f6bb54c927b415b95727c4bb6d9a84c4615ea77d9872911b05 \
    --hash=sha256:f76c21a4b4c72e9e09763d4d1b234afc469c88693152a763ad6786467ef9e79f
future==0.18.3
six==1.13.0 \
    --hash=sha256:1f1b7d42e254082a9db6279deae68afb421ceba6158efa6131de7b3003ee93fd \
    --hash=sha256:30f610279e8b2578cab6db20741130331735c781b56053c59c4076da27f06b66"""
        )
    assert safety([str(requirements_file)]) == 0


def test_editable_url_to_tarball_dependency(tmp_path):
    requirements_file = tmp_path / "requirements.txt"
    with open(requirements_file, "w", encoding="utf-8") as file:
        file.write(
            "-e https://files.pythonhosted.org/packages/6a/11/114c67b0e3c25c19497fde977538339530d8ffa050d6ec9349793f933faa/lockfile-0.10.2.tar.gz"
        )

    assert safety([str(requirements_file)]) == 0


@pytest.mark.xfail(
    reason="cf. https://github.com/Lucas-C/pre-commit-hooks-safety/issues/1"
)
def test_bare_url_to_tarball_dependency(tmp_path):
    requirements_file = tmp_path / "requirements.txt"
    with open(requirements_file, "w", encoding="utf-8") as file:
        file.write(
            "https://files.pythonhosted.org/packages/6a/11/114c67b0e3c25c19497fde977538339530d8ffa050d6ec9349793f933faa/lockfile-0.10.2.tar.gz"
        )

    assert safety([str(requirements_file)]) == 0


def test_requirements_txt_directory(tmp_path):
    requirements_path = tmp_path / "requirements"
    requirements_path.mkdir(exist_ok=True)
    requirements_file = requirements_path / "app.txt"
    with open(requirements_file, "w", encoding="utf-8") as file:    
        file.write("urllib3==1.24.1")

    assert safety([str(requirements_file)]) == EXIT_CODE_VULNERABILITIES_FOUND


def test_pyproject_toml_without_deps(tmp_path):
    pyproject_file = tmp_path / "pyproject.toml"
    with open(pyproject_file, "w", encoding="utf-8") as file:
        file.write(
            """[tool.poetry]
name = "Thing"
version = "1.2.3"
description = "Dummy"
authors = ["Lucas Cimon"]
"""
        )
    assert safety([str(pyproject_file)]) == 0


def test_pyproject_toml_pep_621_format(tmp_path):
    pyproject_file = tmp_path / "pyproject.toml"
    with open(pyproject_file, "w", encoding="utf-8") as file:
        file.write(
            """[project]
name = "Thing"
version = "1.2.3"
description = "Dummy"
authors = [ {name = "Lucas Cimon"} ]

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
"""
        )
    assert safety([str(pyproject_file)]) == 0


def test_pyproject_toml_with_ko_deps(tmp_path):
    pyproject_file = tmp_path / "pyproject.toml"
    with open(pyproject_file, "w", encoding="utf-8") as file:
        file.write(
            """[tool.poetry]
name = "Thing"
version = "1.2.3"
description = "Dummy"
authors = ["Lucas Cimon"]

[tool.poetry.dependencies]
python = "^3.9"
jubatus = "1.0.2"
"""
        )
    assert safety([str(pyproject_file)]) == EXIT_CODE_VULNERABILITIES_FOUND


def test_pyproject_toml_pep_621_format_with_ko_deps(tmp_path):
    pyproject_file = tmp_path / "pyproject.toml"
    with open(pyproject_file, "w", encoding="utf-8") as file:
        file.write(
            """[project]
name = "Thing"
version = "1.2.3"
description = "Dummy"
authors = [ {name = "Lucas Cimon"} ]

requires-python = ">=3.9"

dependencies = ["jubatus==1.0.2"]

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
"""
        )
    assert safety([str(pyproject_file)]) == EXIT_CODE_VULNERABILITIES_FOUND


def test_pyproject_toml_pep_621_dynamic_format_with_ko_deps(tmp_path):
    pyproject_file = tmp_path / "pyproject.toml"
    with open(pyproject_file, "w", encoding="utf-8") as file:
        file.write(
            """[project]
name = "Thing"
version = "1.2.3"
description = "Dummy"
authors = [ {name = "Lucas Cimon"} ]

requires-python = ">=3.9"
dynamic = ["dependencies"]

[tool.poetry.dependencies]
jubatus = "1.0.2"

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
"""
        )
    assert safety([str(pyproject_file)]) == EXIT_CODE_VULNERABILITIES_FOUND


def test_pyproject_toml_with_ko_dev_deps(tmp_path):
    pyproject_file = tmp_path / "pyproject.toml"
    with open(pyproject_file, "w", encoding="utf-8") as file:
        file.write(
            """[tool.poetry]
name = "Thing"
version = "1.2.3"
description = "Dummy"
authors = ["Lucas Cimon"]

[tool.poetry.dependencies]
python = "^3.9"

# Poetry pre-1.2.x style
[tool.poetry.dev-dependencies]
jubatus = "1.0.2"
"""
        )
    assert (
        safety([str(pyproject_file), "--groups=dev"]) == EXIT_CODE_VULNERABILITIES_FOUND
    )


def test_pyproject_toml_pep_621_with_ko_dev_deps(tmp_path):
    pyproject_file = tmp_path / "pyproject.toml"
    with open(pyproject_file, "w", encoding="utf-8") as file:
        file.write(
            """[project]
name = "Thing"
version = "1.2.3"
description = "Dummy"
authors = [ {name = "Lucas Cimon"} ]

requires-python = ">=3.9"

[tool.poetry.group.dev.dependencies]
jubatus = "1.0.2"

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
"""
        )
    assert (
        safety([str(pyproject_file), "--groups=dev"]) == EXIT_CODE_VULNERABILITIES_FOUND
    )


@pytest.mark.parametrize(
    "group_arg,status",
    [
        ("--groups=dev", 0),
        ("--groups=dev,test", EXIT_CODE_VULNERABILITIES_FOUND),
        ("--groups=test", EXIT_CODE_VULNERABILITIES_FOUND),
    ],
)
def test_pyproject_toml_with_groups(tmp_path, group_arg, status):
    pyproject_file = tmp_path / "pyproject.toml"
    with open(pyproject_file, "w", encoding="utf-8") as file:
        file.write(
            """[tool.poetry]
name = "Thing"
version = "1.2.3"
description = "Dummy"
authors = ["Lucas Cimon"]

[tool.poetry.dependencies]
python = "^3.9"

# Poetry 1.2.0 style
[tool.poetry.group.dev.dependencies]
colored = "1.4.2"

[tool.poetry.group.test.dependencies]
insecure-package = "0.1.0"
"""
        )
    assert safety([str(pyproject_file), group_arg]) == status


@pytest.mark.parametrize(
    "group_arg,status",
    [
        ("--groups=dev", 0),
        ("--groups=dev,test", EXIT_CODE_VULNERABILITIES_FOUND),
        ("--groups=test", EXIT_CODE_VULNERABILITIES_FOUND),
    ],
)
def test_pyproject_toml_pep_621_format_with_groups(tmp_path, group_arg, status):
    pyproject_file = tmp_path / "pyproject.toml"
    with open(pyproject_file, "w", encoding="utf-8") as file:
        file.write(
            """[project]
name = "Thing"
version = "1.2.3"
description = "Dummy"
authors = [ {name = "Lucas Cimon"} ]

requires-python = ">=3.9"

[tool.poetry.group.dev.dependencies]
colored = "1.4.2"

[tool.poetry.group.test.dependencies]
insecure-package = "0.1.0"

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
"""
        )
    assert safety([str(pyproject_file), group_arg]) == status


def test_allow_dir_with_requirements_in_name(tmp_path):
    dir_path = tmp_path / "src_requirements_dir"
    dir_path.mkdir(exist_ok=True)
    with open(dir_path / "dummy_file.py", "w", encoding="utf-8") as file:
        file.write("# this is a comment")

    pyproject_file = tmp_path / "pyproject.toml"
    with open(pyproject_file, "w", encoding="utf-8") as file:
        file.write(
            """[tool.poetry]
name = "Thing"
version = "1.2.3"
description = "Dummy"
authors = ["Lucas Cimon"]
"""
        )
    assert safety([str(pyproject_file)]) == 0


def test_allow_file_with_requirements_in_name(tmp_path):
    dir_path = tmp_path / "src"
    dir_path.mkdir(exist_ok=True)
    with open(dir_path / "create_requirements.py", "w", encoding="utf-8") as file:
        file.write("# this is a comment")

    pyproject_file = tmp_path / "pyproject.toml"
    with open(pyproject_file, "w", encoding="utf-8") as file:
        file.write(
            """[tool.poetry]
name = "Thing"
version = "1.2.3"
description = "Dummy"
authors = ["Lucas Cimon"]
"""
        )
    assert safety([str(pyproject_file)]) == 0
