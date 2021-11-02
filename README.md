[![build status](https://github.com/Lucas-C/pre-commit-hooks-safety/workflows/build/badge.svg)](https://github.com/Lucas-C/pre-commit-hooks-safety/actions?query=branch%3Amaster)

A [pre-commit](http://pre-commit.com) hook to check your Python dependencies against [safety-db](//github.com/pyupio/safety-db).

It checks all files containing `requirements` in their name in the repo.

Releases details: [CHANGELOG.md](CHANGELOG.md)

## Usage
```
-   repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.2.2
    hooks:
    -   id: python-safety-dependencies-check
```


## How to Use Arguments
There are a few different arguements that this hook will accept.

The first is the `files` arguement. Simply put which file your dependancies are listed in.
```
-   repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.2.2
    hooks:
    -   id: python-safety-dependencies-check
        files: pyproject.toml
```
The next is the `--ignore` flag. This will ignore a comma seperated list of known security issues. For example
```
-   repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.2.2
    hooks:
    -   id: python-safety-dependencies-check
        args: [--ignore=39153,39652]
```
You can also select between `--full-report` and `--short-report`. By default safety will use the `--full-report` flag so you can omit it for cleaner code.
```
-   repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.2.2
    hooks:
    -   id: python-safety-dependencies-check
        files: pyproject.toml
        args: [--short-report]
```
This will remove the extra detail about what vulnerability was fixed. This can be useful if multiple issues are found and you want to read through less text.  
Of course these can be used in any combination with each other as needed.

For more information look at the [pre-commit](https://pre-commit.com/#passing-arguments-to-hooks) documentation. There you can find some more thorough examples. 
## Alternative local hook
You'll need to `pip install safety` beforehand:
```
-   repo: local
    hooks:
    -   id: python-safety-dependencies-check
        entry: safety
        args: [check, --full-report]
        language: system
        files: requirements
```

## Development

### Setup

    pip install -r dev-requirements.txt
    pre-commit install

### Releasing

1. Bump version in this file, `setup.py` & `.pre-commit-config.yaml`
2. `git commit -nam "Release $version" && git push && git tag $version && git push --tags`
