A pre-commit to check your Python dependencies against [safety-db](//github.com/pyupio/safety-db).

It checks all packages installed, and only the ones local to the current virtualenv if in a virtualenv.

## Usage
```
-   repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    sha: v1.0.8
    hooks:
    -   id: python-safety-dependencies-check
```

In case of a `Error: -r option requires an argument` error, meaning that the default `files` pattern does not match any requirements file in your repo, try to [override it](http://pre-commit.com/#plugins).

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
