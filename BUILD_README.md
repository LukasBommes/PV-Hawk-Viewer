### Create a Release

Update version number in `setup.py`. Commit changes. 
Tag the commit (on master branch) and push tag
```
git tag vx.x.x
git push origin vx.x.x
```
and create a release on GitHub using that tag.

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

### Run locally without installation (for development)
```
python3 -m src.__main__
```
