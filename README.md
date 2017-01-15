# QtAwesome


## Build status
[![Travis](https://travis-ci.org/spyder-ide/qtawesome.svg?branch=master)](https://travis-ci.org/spyder-ide/qtawesome)
[![Appveyor](https://ci.appveyor.com/api/projects/status/un8vnw4628cl6qfu?svg=true)](https://ci.appveyor.com/project/spyder-ide/qtawesome)
[![CircleCI](https://circleci.com/gh/spyder-ide/qtawesome/tree/master.svg?style=shield)](https://circleci.com/gh/spyder-ide/qtawesome/tree/master)
[![Quantified Code](https://www.quantifiedcode.com/api/v1/project/5b42f6edb1ac4465b0e891a4b0144bd8/badge.svg)](https://www.quantifiedcode.com/app/project/5b42f6edb1ac4465b0e891a4b0144bd8)
[![Scrutinizer](https://scrutinizer-ci.com/g/spyder-ide/qtawesome/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/spyder-ide/qtawesome/?branch=master)

## Project information
[![Documentation Status](https://readthedocs.org/projects/qtawesome/badge/?version=latest)](http://qtawesome.readthedocs.org/en/latest/?badge=latest)
[![Join the chat at https://gitter.im/spyder-ide/qtawesome](https://badges.gitter.im/spyder-ide/qtawesome.svg)](https://gitter.im/spyder-ide/qtawesome)

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

