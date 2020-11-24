To release a new version of qtawesome on PyPI:

* git fetch upstream && git checkout master && git merge upstream/master

* Close the current milestone on Github

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

* git push upstream master

* git push upstream --tags
