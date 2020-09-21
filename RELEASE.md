To release a new version of qtawesome on PyPI:

* git fetch upstream && git merge upstream/master

* git clean -xfdi

* Update CHANGELOG.md with

      loghub spyder-ide/qtawesome -m vX.X.X

* Update `_version.py` (set release version, remove 'dev0')

* git add and git commit -m "Release x.x.x"

* Update the most important release packages with

      pip install -U pip setuptools twine wheel

* python setup.py sdist

* python setup.py bdist_wheel

* twine upload dist/*

* git tag -a vX.X.X -m 'Release x.x.x'

* Update `_version.py` (add 'dev0' and increment minor)

* git add and git commit with "Back to work"

* git checkout master

* git merge 0.x and git commit with "Merge from 0.x: Release x.x.x"

* git push upstream master

* git push upstream 0.x

* git push upstream --tags
