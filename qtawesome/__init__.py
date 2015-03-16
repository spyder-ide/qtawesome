"""
PyQtAwesome - use font-awesome in PyQt / PySide applications

This is a port to Python of the C++ QtAwesome by Rick Blommers
"""
from .iconic_font import IconicFont
from .animation import Pulse, Spin


__version__ = '0.1.4'
_resource = {'iconic': None, }


def _instance():
    if _resource['iconic'] is None:
        _resource['iconic'] = IconicFont(('fa', 'fontawesome-4.3.0.ttf', 'fontawesome-4.3.0-charmap.json'),
                                         ('ei', 'elusiveicons-webfont.ttf', 'elusiveicons-webfont-charmap.json'))
    return _resource['iconic']


def icon(*args, **kwargs):
    return _instance().icon(*args, **kwargs)


def icon_stack(*args, **kwargs):
    return _instance().icon_stack(*args, **kwargs)


def load_font(*args, **kwargs):
    return _instance().load_font(*args, **kwargs)


def charmap(prefixed_name):
    prefix, name = prefixed_name.split('.')
    return _instance().charmap[prefix][name]


def font(*args, **kwargs):
    return _instance().font(*args, **kwargs)


def set_custom_icon(*args, **kwargs):
    return _instance().set_custom_icon(*args, **kwargs)
