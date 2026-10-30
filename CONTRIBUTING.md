# Contributing

Thank you for your interest in the evidence ledger schema. The [evidence-ledger-mcp server](https://github.com/matthiaskloft/evidence-ledger-mcp) is a separate implementation; report server bugs there.

## Issues

Issues are welcome: questions, problems with the schema, suggestions for new or changed fields, and pointers to related work we should know about. Please say which schema version an issue is about.

## Pull requests

Pull requests can only be opened by invited collaborators. If you would like to propose a change, please open an issue first; we will discuss it there.

## For collaborators

Install the test dependencies and enable the pre-commit hook once per clone:

```bash
python -m pip install -r requirements-test.txt
git config core.hooksPath .githooks
```

The hook blocks commits that would publish private ledger content or personal email addresses, including a non-noreply commit address. CI runs the same content check on every pull request.

Before opening a pull request, run what CI runs:

```bash
python -m unittest discover -s tests -v
python tools/check_public.py
```

Schema releases are a `schema-vX.Y.Z` tag with a GitHub release; see [CHANGELOG.md](CHANGELOG.md).
