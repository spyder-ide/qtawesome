# History of changes

## Version 0.5 (2018-09-18)

### New features

* Update FontAwesome 4 to 4.7. Its namespace will be `fa` forever.
* Add Material Design icons under the `mdi` namespace
* Add FontAwesome 5 icons under the `fa5` (regular), `fa5s` (solid) and
  `fa5b` (brands) namespaces.

### Issues Closed

* [Issue 93](https://github.com/spyder-ide/qtawesome/issues/93) - Update MDI to 2.7.94 ([PR 95](https://github.com/spyder-ide/qtawesome/pull/95))
* [Issue 88](https://github.com/spyder-ide/qtawesome/issues/88) - Add support for Material Design Icons ([PR 92](https://github.com/spyder-ide/qtawesome/pull/92))
* [Issue 87](https://github.com/spyder-ide/qtawesome/issues/87) - Update FontAwesome to its 5 version ([PR 86](https://github.com/spyder-ide/qtawesome/pull/86))
* [Issue 76](https://github.com/spyder-ide/qtawesome/issues/76) - Error in animation.py when quickly set spinner ([PR 77](https://github.com/spyder-ide/qtawesome/pull/77))
* [Issue 41](https://github.com/spyder-ide/qtawesome/issues/41) - Add .project and .pydevproject to .gitignore ([PR 96](https://github.com/spyder-ide/qtawesome/pull/96))

In this release 5 issues were closed.

### Pull Requests Merged

* [PR 96](https://github.com/spyder-ide/qtawesome/pull/96) - PR: Ignore PyDev project files ([41](https://github.com/spyder-ide/qtawesome/issues/41))
* [PR 95](https://github.com/spyder-ide/qtawesome/pull/95) - PR: Update MDI to 2.7.94 ([93](https://github.com/spyder-ide/qtawesome/issues/93))
* [PR 92](https://github.com/spyder-ide/qtawesome/pull/92) - PR: Add Material Design Icons support ([88](https://github.com/spyder-ide/qtawesome/issues/88))
* [PR 91](https://github.com/spyder-ide/qtawesome/pull/91) - PR: Fix testing facilities
* [PR 86](https://github.com/spyder-ide/qtawesome/pull/86) - PR: Update FontAwesome to 5.3.1 ([87](https://github.com/spyder-ide/qtawesome/issues/87))
* [PR 85](https://github.com/spyder-ide/qtawesome/pull/85) - PR: Update readme to remove funding appeal, harmonize with other readmes and minor fixes
* [PR 81](https://github.com/spyder-ide/qtawesome/pull/81) - PR: Replace qRound (missing in PySide2) with round
* [PR 77](https://github.com/spyder-ide/qtawesome/pull/77) - PR: Fix error when updating animations ([76](https://github.com/spyder-ide/qtawesome/issues/76))
* [PR 72](https://github.com/spyder-ide/qtawesome/pull/72) - PR: Updating FontAwesome to 4.7

In this release 9 pull requests were closed.


----


## Version 0.4.4 (2017-01-28)

### Bugs fixed

**Pull requests**

* [PR 70](https://github.com/spyder-ide/qtawesome/pull/70) - PR: Prevent segfaults when importing QtAwesome out of a of QApplication

In this release 1 pull request was merged


----


## Version 0.4.3 (2017-01-22)

### Bugs fixed

**Pull requests**

* [PR 68](https://github.com/spyder-ide/qtawesome/pull/68) - PR: Include example script into tarball to run tests when the package is installed

In this release 1 pull request was merged


----


## Version 0.4.2 (2017-01-21)

### Bugs fixed

**Issues**

* [Issue 65](https://github.com/spyder-ide/qtawesome/issues/65) - Update Appveyor Badge for new username spyder-ide
* [Issue 64](https://github.com/spyder-ide/qtawesome/issues/64) - Integration with system fonts
* [Issue 51](https://github.com/spyder-ide/qtawesome/issues/51) - Include  doc files in PyPi releases

In this release 3 issues were closed

**Pull requests**

* [PR 67](https://github.com/spyder-ide/qtawesome/pull/67) - PR: Add a way to not verify hash of vendorized fonts
* [PR 66](https://github.com/spyder-ide/qtawesome/pull/66) - PR: Update AppVeyor badge because of move to org account
* [PR 63](https://github.com/spyder-ide/qtawesome/pull/63) - Update manifest template

In this release 3 pull requests were merged


----


## Version 0.4.1 (2017-01-02)

### Bugs fixed

**Pull requests**

* [PR 62](https://github.com/spyder-ide/qtawesome/pull/62) - Improve verification that our fonts are not empty and/or missing

In this release 1 pull request was merged


----


## Version 0.4 (2017/01/01)

### New features

* Add a FontError exception to be able to catch an error on Windows 10, which
  prevents reading fonts not installed in the system.

### Bugs fixed

**Issues**

* [Issue 55](https://github.com/spyder-ide/qtawesome/issues/55) - Add appveyor integration
* [Issue 54](https://github.com/spyder-ide/qtawesome/issues/54) - Add travis ci integration for mac
* [Issue 53](https://github.com/spyder-ide/qtawesome/issues/53) - Add circle ci integration for linux

In this release 3 issues were closed

**Pull requests**

* [PR 61](https://github.com/spyder-ide/qtawesome/pull/61) - PR: Fix errors in CI services
* [PR 60](https://github.com/spyder-ide/qtawesome/pull/60) - PR: Add validation to raise exception when fonts are empty or corrupt
* [PR 57](https://github.com/spyder-ide/qtawesome/pull/57) - PR: Simplify appveyor and circle ci config
* [PR 56](https://github.com/spyder-ide/qtawesome/pull/56) - PR: Add ciocheck and circle ci linux integration
* [PR 50](https://github.com/spyder-ide/qtawesome/pull/50) - PR: Conda installation instructions
* [PR 49](https://github.com/spyder-ide/qtawesome/pull/49) - PR: Remove conda recipe
* [PR 48](https://github.com/spyder-ide/qtawesome/pull/48) - PR: Improve documentation

In this release 7 pull requests were merged
