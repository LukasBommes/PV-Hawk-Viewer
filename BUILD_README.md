### Build and Upload to PyPI

Upgrade build environment
```
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine
```

Build distribution package
```
python3 -m build
```

Upload to PyPI
```
python3 -m twine upload dist/*
```

### Run locally (for development)
```
python3 -m src.__main__
```