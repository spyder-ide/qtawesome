Usage
-----

.. code:: python

   import qtawesome as qta

Use Font Awesome and Elusive Icons.

.. code:: python

    # Get icons by name.
    fa_icon = qta.icon('fa5s.flag')
    fa_button = QtGui.QPushButton(fa_icon, 'Font Awesome!')
    asl_icon = qta.icon('ei.asl')
    elusive_button = QtGui.QPushButton(asl_icon, 'Elusive Icons!')


Apply some styling

.. code:: python

    # Styling icons
    styling_icon = qta.icon('fa5s.music',
                            active='fa5s.balance-scale',
                            color='blue',
                            color_active='orange')

    music_button = QtGui.QPushButton(styling_icon, 'Styling')

Stack multiple icons

.. code:: python

    # Stacking icons
    camera_ban = qta.icon('fa5.camera', 'fa5s.ban',
                          options=[{
                              'scale_factor': 0.5,
                              'active': 'fa5s.balance-scale'
                          }, {
                              'color': 'red'
                          }])
    stack_button = QtGui.QPushButton(camera_ban, 'Stack')
    stack_button.setIconSize(QtCore.QSize(32, 32))

Animations

.. code:: python

    # Spining icons
    spin_button = QtGui.QPushButton(' Spinning icon')
    spin_icon = qta.icon('fa5s.spinner', color='red',
                         animation=qta.Spin(spin_button))
    spin_button.setIcon(spin_icon)

Screenshot

.. image:: ../../qtawesome-screenshot.gif