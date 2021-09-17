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
