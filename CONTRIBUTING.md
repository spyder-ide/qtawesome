# Contributing Guide

QtAwesome is part of the Spyder IDE Github org, and is developed with standard Github flow.

If you're not comfortable with at least the basics of ``git`` and GitHub, we recommend reading beginner tutorials such as [GitHub's Git Guide](https://github.com/git-guides/), its [introduction to basic Git commands](https://guides.github.com/introduction/git-handbook/#basic-git) and its [guide to the fork workflow](https://guides.github.com/activities/forking/), or (if you prefer) their [video equivalents](https://www.youtube.com/githubguides).
However, this contributing guide should fill you in on most of the basics you need to know.

Let us know if you have any further questions, and we look forward to your contributions!


## Reporting Issues

Discover a bug?
Want a new feature?
[Open](https://github.com/spyder-ide/qtawesome/issues/new/choose) an [issue](https://github.com/spyder-ide/qtawesome/issues)!
Make sure to describe the bug or feature in detail, with reproducible examples and references if possible, what you are looking to have fixed/added.
While we can't promise we'll fix everything you might find, we'll certainly take it into consideration, and typically welcome pull requests to resolve accepted issues.


## Setting Up a Development Environment

**Note**: You may need to substitute ``python3`` for ``python`` in the commands below on some Linux distros where ``python`` isn't mapped to ``python3`` (yet).

### Fork and clone the repo

First, navigate to the [project repository](https://github.com/spyder-ide/qtawesome) in your web browser and press the ``Fork`` button to make a personal copy of the repository on your own Github account.
Then, click the ``Clone or Download`` button on your repository, copy the link and run the following on the command line to clone the repo:

```bash
git clone <LINK-TO-YOUR-REPO>
```

Finally, set the upstream remote to the official QtAwesome repo with:

```bash
git remote add upstream https://github.com/spyder-ide/qtawesome.git
```


### Create and activate a fresh environment

Particularly for development installs, we highly recommend you create and activate a virtual environment to avoid any conflicts with other packages on your system or causing any other issues.
Of course, you're free to use any environment management tool of your choice (conda, virtualenvwrapper, pyenv, etc).

To do so with Conda (recommended), simply execute the following:

```bash
conda create -c conda-forge -n qtawesome-env python=3.9
```

And activate it with

```bash
conda activate qtawesome-env
```

With pip/venv, you can create a virtual environment with

```bash
python -m venv qtawesome-env
```

And activate it with the following on Linux and macOS,

```bash
source qtawesome-env/bin/activate
```

or on Windows (cmd),

```cmd
.\qtawesome-env\Scripts\activate.bat
```

Regardless of the tool you use, make sure to remember to always activate your environment before using it.


### Install a Python Qt binding and QtAwesome in editable mode

Before installing QtAwesome itself, make sure you have the Qt binding(s) you wish to develop against.
For example, for PyQt5 on Conda, you'd run with created env activated:

```bash
conda env update --file requirements/environment.yml
```

And then install QtAwesome:

```bash
python -m pip install -e . --no-deps
```

Or for the same using pip, you'd execute:

```bash
python -m pip install pyqt5==5.* PyQtWebEngine==5.*
```

And then install QtAwesome:

```bash
python -m pip install -e .[test]
```

You can then import and use QtAwesome as normal.
When you make changes in your local copy of the git repository, they will be reflected in your installed copy as soon as you re-run Python.



## Deciding Which Branch to Use

When you start to work on a new pull request (PR), you need to be sure that your work is done on top of the correct branch, and that you base your PR on Github against it.

To guide you, issues on Github are marked with a milestone that indicates the correct branch to use: 

* `master` branch: Changes for versions >=`1.x`
* `0.x` branch: Maintainance for versions <= `0.x` (currently no work is being done here)

## Making Your Changes

To start working on a new PR, you need to execute these commands, filling in the branch names where appropriate (``<BASE-BRANCH>`` is the branch you're basing your work against, e.g. ``master``, while ``<FEATURE-BRANCH>`` is the branch you'll be creating to store your changes, e.g. ``fix-icon-bug`` or ``add-icon-support``:

```bash
git checkout <BASE-BRANCH>
git pull upstream <BASE-BRANCH>
git checkout -b <FEATURE-BRANCH>
```

Once you've made and tested your changes, commit them with a descriptive, unique message of 74 characters or less written in the imperative tense, with a capitalized first letter and no period at the end.
Try to make your commit message understandable on its own, giving the reader a high-level idea of what your changes accomplished without having to dig into the diffs.
For example:

```bash
git commit -am "Fix bug using custom font on Windows"
```

If your changes are complex (more than a few dozen lines) and can be broken into discrete steps/parts, its often a good idea to make multiple commits as you work.
On the other hand, if your changes are fairly small (less than a dozen lines), its usually better to make them as a single commit, and then use the ``git -a --amend`` (followed by ``git push -f``, if you've already pushed your work) if you spot a bug or a reviewer requests a change.

These aren't hard and fast rules, so just use your best judgment, and if there does happen to be a significant issue we'll be happy to help.


## Running the Tests

Once you've made your changes (or ideally, before), you'll want to run the full test suite and write new tests of your own, if you haven't already done so.

This package uses the [Pytest](https://pytest.org) framework for its unit and integration tests, which are located inside the package alongside the tested code, in the ``tests/`` subdirectory.
We **strongly** suggest you run the full test suite before every commit (it should only take a few seconds to run on most machines).

In general, any new major functionality should come with tests, and we welcome contributing to expand our coverage, increase reliability, and ensure we don't experience any regressions.
If you need help writing tests, please let us know, and we'll be happy to guide you.

To run the tests, install the development dependencies as above, and then simply execute

```bash
pytest -vv -x
```


## Pushing your Changes

Now that your changes are ready to go, you'll need to push them to the appropriate remote.
All contributors, including core developers, should push to their personal fork and submit a PR from there, to avoid cluttering the upstream repo with feature branches.
To do so, run:

```bash
git push -u origin <FEATURE-BRANCH>
```

Where ``<FEATURE-BRANCH>`` is the name of your feature branch, e.g. ``fix-icon-bug``.



## Submitting a Pull Request

Finally, create a pull request to the [spyder-ide/qtawesome repository](https://github.com/spyder-ide/qtawesome/) on Github.
Make sure to set the target branch to the one you based your PR off of (``master`` or ``X.x``).

We'll then review your changes, and after they're ready to go, your work will become an official part of Qtawesome.

Thanks for taking the time to read and follow this guide, and we look forward to your contributions!
