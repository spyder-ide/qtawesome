# QtAwesome

## Project information

[![Documentation Status](https://readthedocs.org/projects/qtawesome/badge/?version=latest)](http://qtawesome.readthedocs.org/en/latest/?badge=latest)
[![Join the chat at https://gitter.im/spyder-ide/public](https://badges.gitter.im/spyder-ide/spyder.svg)](https://gitter.im/spyder-ide/public)
[![OpenCollective Backers](https://opencollective.com/spyder/backers/badge.svg?color=blue)](#backers)
[![OpenCollective Sponsors](https://opencollective.com/spyder/sponsors/badge.svg?color=blue)](#sponsors)

## Build status

[![Appveyor](https://ci.appveyor.com/api/projects/status/un8vnw4628cl6qfu?svg=true)](https://ci.appveyor.com/project/spyder-ide/qtawesome)
[![CircleCI](https://circleci.com/gh/spyder-ide/qtawesome/tree/master.svg?style=shield)](https://circleci.com/gh/spyder-ide/qtawesome/tree/master)
[![codecov](https://codecov.io/gh/spyder-ide/qtawesome/branch/master/graph/badge.svg)](https://codecov.io/gh/spyder-ide/qtawesome)

----

## Important Announcement: Spyder is unfunded!

Since mid November/2017, [Anaconda, Inc](https://www.anaconda.com/) has
stopped funding Spyder development, after doing it for the past 18
months. Because of that, development will focus from now on maintaining
Spyder 3 at a much slower pace than before.

If you want to contribute to maintain Spyder, please consider donating at

https://opencollective.com/spyder

We appreciate all the help you can provide us and can't thank you enough for
supporting the work of Spyder devs and Spyder development.

If you want to know more about this, please read this
[page](https://github.com/spyder-ide/spyder/wiki/Anaconda-stopped-funding-Spyder).

----
## Description

QtAwesome enables iconic fonts such as Font Awesome and Elusive Icons in PyQt
and PySide applications.

It started as a Python port of the [QtAwesome](https://github.com/Gamecreature/qtawesome)
C++ library by Rick Blommers.

## Installation

Using `pip`:

Make sure you have [pip installed](https://pip.readthedocs.org/en/stable/installing/) and run:

```
pip install qtawesome
```

Using `conda`:

```
conda install qtawesome
```

## Examples

```python
import qtawesome as qta
```

- Use Font Awesome and Elusive Icons.

```python
# Get icons by name.
fa_icon = qta.icon('fa.flag')
fa_button = QtGui.QPushButton(fa_icon, 'Font Awesome!')

asl_icon = qta.icon('ei.asl')
elusive_button = QtGui.QPushButton(asl_icon, 'Elusive Icons!')
```

- Apply some styling

```python
# Styling icons
styling_icon = qta.icon('fa.music',
                        active='fa.legal',
                        color='blue',
                        color_active='orange')
music_button = QtGui.QPushButton(styling_icon, 'Styling')
```

- Stack multiple icons

```python
# Stacking icons
camera_ban = qta.icon('fa.camera', 'fa.ban',
                      options=[{'scale_factor': 0.5,
                                'active': 'fa.legal'},
                               {'color': 'red'}])
stack_button = QtGui.QPushButton(camera_ban, 'Stack')
stack_button.setIconSize(QtCore.QSize(32, 32))
```

- Animations

```python
# Spining icons
spin_button = QtGui.QPushButton(' Spinning icon')
spin_icon = qta.icon('fa.spinner', color='red',
                     animation=qta.Spin(spin_button))
spin_button.setIcon(spin_icon)
```

- Screenshot

![QtAwesome screenshot](qtawesome-screenshot.gif)

## Other features

- QtAwesome comes bundled with Font Awesome and Elusive Icons, but it can also
  be used with other iconic fonts. The `load_font` function allows to load
  other fonts dynamically.
- QtAwesome relies on the [QtPy](https://github.com/spyder-ide/qtpy.git)
  project as a compatibility layer on the top ot PyQt or PySide.

## License

MIT License. Copyright 2015 - The Spyder development team.
See the [LICENSE](LICENSE) file for details.

The Font Awesome and Elusive Icons fonts are licensed under the SIL Open Font License.

## Contributing

Everyone is welcome to contribute!

## Backers

Support us with a monthly donation and help us continue our activities.

[![Backers](https://opencollective.com/spyder/backers.svg)](https://opencollective.com/spyder#support)

## Sponsors

Become a sponsor to get your logo on our README on Github.

[![Sponsors](https://opencollective.com/spyder/sponsors.svg)](https://opencollective.com/spyder#support)
