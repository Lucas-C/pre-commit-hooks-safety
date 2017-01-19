A [pre-commit](http://pre-commit.com) hook to check your Python dependencies against [safety-db](//github.com/pyupio/safety-db).

It checks all files containing `requirements` in their name in the repo.

## Usage
```
-   repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    sha: v1.0.10
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
