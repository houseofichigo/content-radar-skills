# Contributing

Keep each skill independently discoverable and narrowly scoped. Shared brand data belongs in the project-level `profile.md`; reusable templates required at runtime must also be bundled inside the skill that consumes them.

Before opening a change, run:

```bash
python3 scripts/build_dist.py
python3 scripts/validate_suite.py
python3 -m unittest discover -s tests -v
```

Do not commit credentials, private brand profiles, fetched web content, or generated monitoring reports.
