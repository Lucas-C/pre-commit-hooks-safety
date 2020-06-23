[![](https://travis-ci.org/Lucas-C/pre-commit-hooks-safety.svg?branch=master)](https://travis-ci.org/Lucas-C/pre-commit-hooks-safety)

A [pre-commit](http://pre-commit.com) hook to check your Python dependencies against [safety-db](//github.com/pyupio/safety-db).

It checks all files containing `requirements` in their name in the repo.

## Usage
```
-   repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    sha: v1.1.2
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

1. Bump version in this file and `.pre-commit-config.yaml`
2. `git commit -nam "Release $version" && git push && git tag $version && git push --tags`
