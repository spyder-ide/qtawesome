.. image:: https://pypip.in/version/QtAwesome/badge.svg
   :target: https://pypi.python.org/pypi/QtAwesome/
   :alt: Latest PyPI version

.. image:: https://pypip.in/download/QtAwesome/badge.svg
   :target: https://pypi.python.org/pypi/QtAwesome/
   :alt: Number of PyPI downloads

.. image:: https://pypip.in/py_versions/QtAwesome/badge.svg
   :target: https://pypi.python.org/pypi/QtAwesome/
   :alt: Supported python version
   
.. image:: https://pypip.in/license/QtAwesome/badge.svg

.. image:: https://travis-ci.org/spyder-ide/QtAwesome.svg?branch=master
   :target: https://travis-ci.org/spyder-ide/QtAwesome
   :alt: Travis-CI build status

QtAwesome - Iconic Fonts in PyQt and PySide applications
========================================================

Description
-----------

QtAwesome enables iconic fonts such as `Font Awesome`_ and `Elusive Icons`_ in your PyQt and PySide application.

It is a port to Python - PyQt / PySide of the `QtAwesome`_ C++ library by Rick Blommers.


License
-------

MIT License. Copyright 2015 - The Spyder development team

The *Font Awesome* and *Elusive Icons* fonts are licensed under the `SIL Open Font License`_.


Installation
------------
.. code-block:: python

    pip install QtAwesome


Examples
--------

.. code-block:: python

    import qtawesome as qta


- Use Font Awesome and Elusive Icons.
.. code-block:: python

    # Get icons by name.
    fa_icon = qta.icon('fa.flag')
    fa_button = QtGui.QPushButton(fa_icon, 'Font Awesome!')

    asl_icon = qta.icon('ei.asl')
    elusive_button = QtGui.QPushButton(asl_icon, 'Elusive Icons!')

- Apply some styling
.. code-block:: python

    styling_icon = qta.icon('fa.music',
                            active='fa.legal',
                            color='blue',
                            color_active='orange')
    music_button = QtGui.QPushButton(styling_icon, 'Styling')


- Stack multiple icons
.. code-block:: python

    # Stack icons
    camera_ban = qta.icon_stack(['fa.camera', 'fa.ban'],
                                options=[{'scale_factor': 0.5,
                                          'active': 'fa.legal'},
                                         {'color': 'red'}])
    stack_button = QtGui.QPushButton(camera_ban, 'Stack')
    stack_button.setIconSize(QtCore.QSize(32, 32))


- Animations
.. code-block:: python

    # Spin icons
    spin_button = QtGui.QPushButton(' Spinning icon')
    spin_icon = qta.icon('fa.spinner', color='red',
                         animation=qta.Spin(spin_button))
    spin_button.setIcon(spin_icon)


Other features
--------------

- The API is pluggable so as to enable custom painters and animations.
- While QtAwesome embeds Font Awesome and Elusive Icons, it can also be used with other iconic fonts. A ``load_font`` function is available. A ttf font and a json character map for icon names must be provided. 


.. _Font Awesome: http://fortawesome.github.io/Font-Awesome/
.. _Elusive Icons: http://elusiveicons.com/
.. _QtAwesome: https://github.com/gamecreature/QtAwesome
.. _SIL Open Font License : http://scripts.sil.org/OFL

