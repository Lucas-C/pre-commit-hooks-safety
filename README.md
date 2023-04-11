[![build status](https://github.com/Lucas-C/pre-commit-hooks-safety/workflows/build/badge.svg)](https://github.com/Lucas-C/pre-commit-hooks-safety/actions?query=branch%3Amaster)

A [pre-commit](http://pre-commit.com) hook to check your Python dependencies against [safety-db](//github.com/pyupio/safety-db).

It checks all files containing `requirements` in their name in the repo.

Releases details: [CHANGELOG.md](CHANGELOG.md)

Note that **telemetry data will be sent with every Safety call**. These data are anonymous and not sensitive. This includes the Python version, the Safety command used (check/license/review), and the Safety options used (without their values). Users can disable this functionality by adding the `--disable-telemetry` flag.

## Usage
```yaml
-   repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.3.1
    hooks:
    -   id: python-safety-dependencies-check
```

## How to Use Arguments
There are a few different arguements that this hook will accept.

The first is the `files` arguement. Simply put which file your dependancies are listed in.
```yaml
-   repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.3.1
    hooks:
    -   id: python-safety-dependencies-check
        files: pyproject.toml
```
The next is the `--ignore` flag. This will ignore a comma seperated list of known security issues. For example
```yaml
-   repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.3.1
    hooks:
    -   id: python-safety-dependencies-check
        args: ["--ignore=39153,39652"]
```
You can also select between `--full-report` and `--short-report`. By default safety will use the `--full-report` flag so you can omit it for cleaner code.
```yaml
-   repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.3.1
    hooks:
    -   id: python-safety-dependencies-check
        files: pyproject.toml
        args: ["--short-report"]
```
This will remove the extra detail about what vulnerability was fixed. This can be useful if multiple issues are found and you want to read through less text.
Of course these can be used in any combination with each other as needed.

For more information look at the [pre-commit](https://pre-commit.com/#passing-arguments-to-hooks) documentation. There you can find some more thorough examples.
You may for example want to use `always_run: true` in order to systematically run this hook, even when no dependency files have been modified.

## Supported files

`requirements` files are supported with any ending (e.g. .txt) and you can pass multiple files to be checked.

`pyproject.toml` files are only supported with a single file per invokation. If you have subpackages with one `pyproject.toml` each you need to invoke the hook multiple times.

Currently only [`poetry`](https://python-poetry.org/) is a supported package mangers for `pyproject.toml` files. When using a `pyproject.toml` file you need to provide [`poetry`](https://python-poetry.org/) via your PATH and have at least version 1.2 installed.

A mix of both file types is not supported.

## Alternative local hook
You'll need to `pip install safety` beforehand:
```yaml
-   repo: local
    hooks:
    -   id: python-safety-dependencies-check
        name: safety
        entry: safety
        args: [check, --full-report, --file]
        language: system
        files: requirements
```

## Development

### Setup

    pip install -r dev-requirements.txt
    pre-commit install

### Releasing

1. Bump version in this `README.md` file, `setup.py`, `.pre-commit-config.yaml` & `CHANGELOG.md`
2. `git commit -nam "Release $version" && git push && git tag $version && git push --tags`
3. Create a GitHub release
