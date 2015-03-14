QtAwesome - Iconic Fonts in PyQt and PySide applications
========================================================

Description
-----------

QtAwesome enables iconic fonts such as [Font Awesome](http://fortawesome.github.io/Font-Awesome/) and [Elusive Icons](http://elusiveicons.com/) in your PyQt and PySide application.

It is a port to Python - PyQt / PySide of the [QtAwesome](https://github.com/gamecreature/QtAwesome) C++ library by Rick Blommers.


License
-------

MIT License. Copyright 2015 - The Spyder development team

The *Font Awesome* and *Elusive Icons* fonts are licensed under the SIL Open Font License - [http://scripts.sil.org/OFL](http://scripts.sil.org/OFL)

Installation
------------
```python
pip install qtawesome
```

Examples
--------

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
styling_icon = qta.icon('fa.music',
                         active='fa.legal',
                         color='blue',
                         color_active='orange')
music_button = QtGui.QPushButton(styling_icon, 'Styling')
```

- Stack multiple icons
```python
# Stack icons
camera_ban = qta.icon_stack(['fa.camera', 'fa.ban'],
                            options=[{'scale_factor': 0.5,
                                      'active': 'fa.legal'},
                                     {'color': 'red'}])
stack_button = QtGui.QPushButton(camera_ban, 'Stack')
stack_button.setIconSize(QtCore.QSize(32, 32))
```

- Animations
```python
# Spin icons
spin_button = QtGui.QPushButton(' Spinning icon')
spin_icon = qta.icon('fa.spinner', color='red',
                     animation=qta.Spin(spin_button))
spin_button.setIcon(spin_icon)
```
Other features
--------------

- The API is pluggable so as to enable custom painters and animations.
- While QtAwesome embeds Font Awesome and Elusive Icons, it can also be used with other iconic fonts. A `load_font` function is available. A ttf font and a json character map for icon names must be provided. 

