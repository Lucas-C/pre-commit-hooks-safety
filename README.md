A pre-commit to check your Python dependencies against [safety-db](//github.com/pyupio/safety-db).

It checks all packages installed, and only the ones local to the current virtualenv if in a virtualenv.

## Usage
```
-   repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    sha: v1.0.9
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
```
