## Instructions to release a new QtAwesome version

To release a new version of QtAwesome (on PyPI and Conda-forge) follow these steps

### Prerequisites

In order to do a release, you need to have:

* An environment with the packages required to do the release (`loghub`, `pip`, `setuptools`, `twine`, `wheel`). If using `conda`, you can create a `release` environment with

      conda create -n release python=3.9
      conda activate release
      pip install -U pip setuptools twine wheel loghub

* Cloned repository (usually your fork with an `upstream` remote pointing to the project original repo)

* The corresponding credentials (PyPI, GitHub, etc).

### PyPI

* Update local repo with

      git fetch upstream && git checkout master && git merge upstream/master

* Close the current [milestone on GitHub](https://github.com/spyder-ide/qtawesome/milestones)

* Clean your local repo with (selecting option 1)

      git clean -xfdi

* Update `CHANGELOG.md` with

      loghub spyder-ide/qtawesome -m vX.Y.Z

* Update `_version.py` (set release version, remove 'dev0'):

      git add . && git commit -m "Release X.Y.Z"

* Update the most important release packages with

      pip install -U pip setuptools twine wheel loghub

* Create source distribution with

      python setup.py sdist

* Create wheel with

      python setup.py bdist_wheel

* Check generated files with

      twine check dist/*

* Upload generated files with

      twine upload dist/*

* Create release tag with

      git tag -a vX.Y.Z -m "Release X.Y.Z"

* Update `_version.py` (add 'dev0' and increment minor)

* Create `Back to work` commit with

      git add . && git commit -m "Back to work"

* Push changes and tag with

      git push upstream master && git push upstream --tags

* Create a [GitHub Release](https://github.com/spyder-ide/qtawesome/releases) (`Draft a new release` and `Publish release`). You can use the `Auto generate release notes` as a base template for the release description and to that add a link to the Changelog (the new release related info).

### Conda-forge

* After doing the release on PyPI check for the `regro-cf-autotick-bot` automatic PR on the [QtAwesome feedstock repo](https://github.com/conda-forge/qtawesome-feedstock/pulls). Review it, check if any dependency or changes are needed and merge it.
