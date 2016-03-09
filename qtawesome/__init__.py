r"""
qtawesome
=========

Font-Awesome and other iconic fonts for PyQt / PySide applications.

.. currentmodule:: qtawesome

.. autosummary::
   :toctree: _generate

   icon
   load_font
   charmap
   font
   set_defaults
"""

from .iconic_font import IconicFont, set_global_defaults
from .animation import Pulse, Spin
from ._version import version_info, __version__

_resource = { 'iconic': None }


def _instance():
    """
    Return the singleton instance of IconicFont.

    Functions ``icon``, ``load_font``, ``charmap``, ``font`` and
    ``set_defaults`` all rebind to methods of the singleton instance of IconicFont.
    """
    if _resource['iconic'] is None:
        _resource['iconic'] = IconicFont(
            ('fa', 'fontawesome-webfont.ttf', 'fontawesome-webfont-charmap.json'),
            ('ei', 'elusiveicons-webfont.ttf', 'elusiveicons-webfont-charmap.json')
        )
    return _resource['iconic']


def icon(*names, **kwargs):
    """
    Return a QIcon object corresponding to the provided icon name(s).

    This function is the main interface of qtawesome. 

    It can be used to create a QIcon instance from a single glyph 
    or from a list of glyphs that are displayed on the top of each other.
    Such icon stacks are generally used to combine multiple glyphs to make
    more complex icons.

    Glyph names are specified by strings, of the form ``prefix.name``.
    The ``prefix`` corresponds to the font to be used and ``name`` is the
    name of the icon.

     - The prefix corresponding to Font-Awesome is 'fa'
     - The prefix corresponding to Elusive-Icons is 'ei'

    When requesting a single glyph, options (such as color or positional offsets)
    can be passed as keyword arguments::

        import qtawesome as qta

        music_icon = qta.icon('fa.music', color='blue', color_active='orange')

    When requesting multiple glyphs, the `options` keyword argument contains the
    list of option dictionaries to be used for each glyph::

        camera_ban = qta.icon('fa.camera', 'fa.ban', options=[{
                'scale_factor': 0.5,
                'active': 'fa.legal'
            }, {
                'color': 'red',
                'opacity': 0.7
            }])

    Qt's ``QIcon`` object has four modes

        - ``Normal``: The user is not interacting with the icon, but the
          functionality represented by the icon is available.
        - ``Disabled``: The functionality corresponding to the icon is not
          available.
        - ``Active``: The functionality corresponding to the icon is available.
          The user is interacting with the icon, for example, moving the mouse
          over it or clicking it.
        - ``Selected``: The item represented by the icon is selected.
 
    The glyph for the Normal mode is the one specified with the main positional
    argument.

     - ``color``: icon color in the ``Normal`` mode.

    The following four options will apply to the icon regardless of the mode.

     - ``offset``: tuple (x, y) corresponding to the horizontal and vertical
       offsets for the glyph, specified as a proportion of the icon size.
     - ``animation``: animation object for the icon.
     - ``scale_factor``: multiplicative scale factor to be used for the glyph. 

    The following options apply to the different modes of the icon

     - ``active``: name of the glyph to be used when the icon is ``Active``.
     - ``color_active``: the corresponding icon color.

     - ``disabled``: name of the glyph to be used when the icon is ``Disabled``.
     - ``color_disabled``: the corresponding icon color.

     - ``selected``: name of the glyph to be used when the icon is ``Selected``.
     - ``color_selected``: the corresponding icon color.

    Default values for these options can be specified via the function
    ``set_defaults``. If unspecified, the default defaults are::

        {
            'opacity': 1.0,
            'scale_factor': 1.0
            'color': QColor(50, 50, 50),
            'color_disabled': QColor(150, 150, 150),
        }

    If no default value is provided for ``active``, ``disabled`` or ``selected``
    the glyph specified for the ``Normal`` mode will be used.

    """
    return _instance().icon(*names, **kwargs)


def load_font(prefix, ttf_filename, charmap_filename, directory=None):
    """
    Loads a font file and the associated charmap.

    If ``directory`` is None, the files will be looked for in ``./fonts/``.

    Parameters
    ----------
    prefix: str
        Prefix string to be used when accessing a given font set
    ttf_filename: str
        Ttf font filename
    charmap_filename: str
        Character map filename
    directory: str or None, optional
        Directory for font and charmap files

    Example
    -------
    The spyder ide uses qtawesome and uses a custom font for spyder-specific
    icons::

        qta.load_font('spyder', 'spyder.ttf', 'spyder-charmap.json')

    """
    return _instance().load_font(prefix, ttf_filename, charmap_filename, directory)


def charmap(prefixed_name):
    """
    Return the character map used for a given font.

    Returns
    -------
    return_value: dict
        The dictionary mapping the icon names to the corresponding unicode character.

    """
    prefix, name = prefixed_name.split('.')
    return _instance().charmap[prefix][name]


def font(prefix, size):
    """
    Return the font corresponding to the specified prefix.

    This can be used to render text using the iconic font directly::

        import qtawesome as qta
        from qtpy import QtWidgets

        label = QtWidgets.QLabel(unichr(0xf19c) + ' ' + 'Label')
        label.setFont(qta.font('fa', 16))

    Parameters
    ----------
    prefix: str
        prefix string of the loaded font
    size: int
        size for the font

    """
    return _instance().font(prefix, size)


def set_defaults(**kwargs):
    """
    Set default options for icons.

    The valid keyword arguments are:

    'active', 'animation', 'color', 'color_active', 'color_disabled',
    'color_selected', 'disabled', 'offset', 'scale_factor', 'selected'.

    """
    return set_global_defaults(**kwargs)

