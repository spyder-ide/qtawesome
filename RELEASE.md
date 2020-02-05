To release a new version of qtawesome on PyPI:

* Close Github milestone

* git fetch upstream && git merge upstream/master

* git clean -xfdi

* Update Changelog

* Update _version.py (set release version, remove 'dev')

* git add and git commit with "Release x.x.x"

* python setup.py sdist

* python setup.py bdist_wheel

* twine upload dist/*

* git tag -a vX.X.X -m 'Release x.x.x'

* Update _version.py (add 'dev0' and increment minor)

* git add and git commit with "Back to work"

* git push upstream master

* git push upstream --tags
