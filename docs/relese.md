# Release

Tag the version and remove the dev suffix

```bash
bumpversion release
```

Create packages and push them to pypi
```bash
python setup.py sdist bdist_wheel upload
```

Create a new dev snapshot
```bash
bumpversion --no-tag minor
```
