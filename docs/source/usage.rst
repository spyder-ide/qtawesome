Usage
-----

Supported Fonts
~~~~~~~~~~~~~~~

QtAwesome identifies icons by their **prefix** and their **icon name**, separated by a *period* (``.``) character.

The following prefixes are currently available to use:

-  `FontAwesome`_:

   -  FA 5.9.0 features 1,534 free icons in different styles:

      -  ``fa5`` prefix has `151 icons in the "regular" style.`_
      -  ``fa5s`` prefix has `935 icons in the "solid" style.`_
      -  ``fa5b`` prefix has `413 icons of various brands.`_

   -  ``fa`` is the legacy `FA 4.7 version with its 675 icons`_ but
      **all** of them (*and more!*) are part of FA 5.x so you should
      probably use the newer version above.

-  ``ei`` prefix holds `Elusive Icons 2.0 with its 304 icons`_.

-  ``mdi`` prefix holds `Material Design Icons 4.5.95 with its 4595
   icons.`_

.. _FontAwesome: https://fontawesome.com
.. _151 icons in the "regular" style.: https://fontawesome.com/icons?d=gallery&s=regular&v=5.0.0,5.0.1,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.0.10,5.0.11,5.0.12,5.0.13,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.5.0,5.6.0,5.6.1,5.6.3&m=free
.. _915 icons in the "solid" style.: https://fontawesome.com/icons?d=gallery&s=solid&v=5.0.0,5.0.1,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.0.10,5.0.11,5.0.12,5.0.13,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.5.0,5.6.0,5.6.1,5.6.3&m=free
.. _414 icons of various brands.: https://fontawesome.com/icons?d=gallery&s=brands&v=5.0.0,5.0.1,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.0.10,5.0.11,5.0.12,5.0.13,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.5.0,5.6.0,5.6.1,5.6.3&m=free
.. _FA 4.7 version with its 675 icons: https://fontawesome.com/v4.7.0/icons/
.. _Elusive Icons 2.0 with its 304 icons: http://elusiveicons.com/icons/
.. _Material Design Icons 4.5.95 with its 4595 icons.: https://cdn.materialdesignicons.com/4.5.95/

Examples
~~~~~~~~

.. code:: python

   import qtawesome as qta

-  Use Font Awesome, Elusive Icons or Material Design Icons:

.. code:: python

   # Get FontAwesome 5.x icons by name in various styles:
   fa5_icon = qta.icon('fa5.flag')
   fa5_button = QtWidgets.QPushButton(fa5_icon, 'Font Awesome! (regular)')
   fa5s_icon = qta.icon('fa5s.flag')
   fa5s_button = QtWidgets.QPushButton(fa5s_icon, 'Font Awesome! (solid)')
   fa5b_icon = qta.icon('fa5b.github')
   fa5b_button = QtWidgets.QPushButton(fa5b_icon, 'Font Awesome! (brands)')

   # or Elusive Icons:
   asl_icon = qta.icon('ei.asl')
   elusive_button = QtWidgets.QPushButton(asl_icon, 'Elusive Icons!')

   # or Material Design Icons:
   apn_icon = qta.icon('mdi.access-point-network')
   mdi_button = QtWidgets.QPushButton(apn_icon, 'Material Design Icons!')

-  Apply some styling:

.. code:: python

   # Styling icons
   styling_icon = qta.icon('fa5s.music',
                           active='fa5s.balance-scale',
                           color='blue',
                           color_active='orange')
   music_button = QtWidgets.QPushButton(styling_icon, 'Styling')

-  Stack multiple icons:

.. code:: python

   # Stacking icons
   camera_ban = qta.icon('fa5s.camera', 'fa5s.ban',
                         options=[{'scale_factor': 0.5,
                                   'active': 'fa5s.balance-scale'},
                                  {'color': 'red'}])
   stack_button = QtWidgets.QPushButton(camera_ban, 'Stack')
   stack_button.setIconSize(QtCore.QSize(32, 32))

-  Animations:

.. code:: python

   # Spining icons
   spin_button = QtWidgets.QPushButton(' Spinning icon')
   spin_icon = qta.icon('fa5s.spinner', color='red',

Screenshot
~~~~~~~~~~

.. image:: ../../qtawesome-screenshot.gif
