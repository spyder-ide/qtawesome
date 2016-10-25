r"""

Iconic Font
===========

A lightweight module handling iconic fonts.

It is designed to provide a simple way for creating QtGui.QIcons from glyphs.

From a user's viewpoint, the main entry point is the ``IconicFont`` class which
contains methods for loading new iconic fonts with their character map and
methods returning instances of ``QtGui.QIcon``.

"""

from __future__ import print_function

import json
import os
import yaml

from six import unichr

from .manifest import QtCore, QtGui

_defaultOptions = {
    'color': QtGui.QColor(50, 50, 50),
    'colorDisabled': QtGui.QColor(150, 150, 150),
    'opacity': 1.0,
    'scaleFactor': 1.0,
}


def getDefaultFontDirectory():
    """:return (str) the path to the fonts directory"""
    directory = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'fonts')
    return directory


def writeCharmap(iconsYaml, ttfFile=None, jsonFile=None, directory=None):
    """
    Writes out the charmap file for a given ttf file.

    To update font-awesome or elusive icons, one must

    - replace the ttf font file with the new version
    - regenerate the json charmap with the `icons.yml` file from the upstream
      repository:

    :param iconsYaml: A required file path to the  yaml file. Often in the sources dir
    :param ttfFile:  The filepath to the ttf file. Optional if jsonFile is provided.
    :param jsonFile: The jsonFile to write to. Optional if ttfFile is provided
    :param directory: The directory to write to. Defaults to the included fonts dir.
    :return: the path to the written json file
    """
    assert ttfFile or jsonFile, "You must provide either a ttf file or a json file to write to"
    if not jsonFile:
        directory = directory if directory else getDefaultFontDirectory()
        ttf, ext = os.path.splitext(os.path.basename(ttfFile))
        jsonFile = os.path.join(directory, ttf + '-charmap.json')

    with open(iconsYaml, 'r') as file:
        icons = yaml.load(file)['icons']

    charmap = {icon['id']: icon['unicode'] for icon in icons}

    for icon in icons:
        if 'aliases' in icon:
            for name in icon['aliases']:
                charmap[name] = icon['unicode']

    with open(jsonFile, 'w') as file:
        json.dump(charmap, file, indent=4, sort_keys=True)

    return jsonFile


def setGlobalDefaults(**kwargs):
    """Set global defaults for the options passed to the icon painter."""

    validOptions = [
        'active', 'selected', 'disabled', 'on', 'off',
        'onActive', 'onSelected', 'onDisabled',
        'offActive', 'offSelected', 'offDisabled',
        'color', 'colorOn', 'colorOff',
        'colorActive', 'colorSelected', 'colorDisabled',
        'colorOnSelected', 'colorOnActive', 'colorOnDisabled',
        'colorOffSelected', 'colorOffActive', 'colorOffDisabled',
        'animation', 'offset', 'scaleFactor',
    ]

    for kw in kwargs:
        if kw in validOptions:
            _defaultOptions[kw] = kwargs[kw]
        else:
            error = "Invalid option '{0}'".format(kw)
            raise KeyError(error)


class CharIconPainter:
    """Char icon painter."""

    def paint(self, iconic, painter, rect, mode, state, options):
        """Main paint method."""
        for opt in options:
            self._paintIcon(iconic, painter, rect, mode, state, opt)

    def _paintIcon(self, iconic, painter, rect, mode, state, options):
        """Paint a single icon."""
        painter.save()
        color = options['color']
        char = options['char']

        color_options = {
            QtGui.QIcon.On: {
                QtGui.QIcon.Normal: (options['colorOn'], options['on']),
                QtGui.QIcon.Disabled: (options['colorOnDisabled'],
                                       options['onDisabled']),
                QtGui.QIcon.Active: (options['colorOnActive'],
                                     options['onActive']),
                QtGui.QIcon.Selected: (options['colorOnSelected'],
                                       options['onSelected'])
            },

            QtGui.QIcon.Off: {
                QtGui.QIcon.Normal: (options['colorOff'], options['off']),
                QtGui.QIcon.Disabled: (options['colorOffDisabled'],
                                       options['offDisabled']),
                QtGui.QIcon.Active: (options['colorOffActive'],
                                     options['offActive']),
                QtGui.QIcon.Selected: (options['colorOffSelected'],
                                       options['offSelected'])
            }
        }

        color, char = color_options[state][mode]

        painter.setPen(QtGui.QColor(color))

        # A 16 pixel-high icon yields a font size of 14, which is pixel perfect
        # for font-awesome. 16 * 0.875 = 14
        # The reason why the glyph size is smaller than the icon size is to
        # account for font bearing.

        draw_size = 0.875 * QtCore.qRound(rect.height() * options['scaleFactor'])
        prefix = options['prefix']

        # Animation setup hook
        animation = options.get('animation')
        if animation is not None:
            animation.setup(self, painter, rect)

        painter.setFont(iconic.font(prefix, draw_size))
        if 'offset' in options:
            rect = QtCore.QRect(rect)
            rect.translate(options['offset'][0] * rect.width(),
                           options['offset'][1] * rect.height())

        painter.setOpacity(options.get('opacity', 1.0))

        painter.drawText(rect, QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter, char)
        painter.restore()


class CharIconEngine(QtGui.QIconEngine):
    """Specialization of QtGui.QIconEngine used to draw font-based icons."""

    def __init__(self, iconic, painter, options):
        super(CharIconEngine, self).__init__()
        self.iconic = iconic
        self.painter = painter
        self.options = options

    def paint(self, painter, rect, mode, state):
        self.painter.paint(
            self.iconic, painter, rect, mode, state, self.options)

    def pixmap(self, size, mode, state):
        pm = QtGui.QPixmap(size)
        pm.fill(QtCore.Qt.transparent)
        self.paint(QtGui.QPainter(pm), QtCore.QRect(QtCore.QPoint(0, 0), size), mode, state)
        return pm


class IconicFont(QtCore.QObject):
    """Main class for managing iconic fonts."""

    def __init__(self, *args):
        """IconicFont Constructor.

        Parameters
        ----------
        ``*args``: tuples
            Each positional argument is a tuple of 3 or 4 values:
            - The prefix string to be used when accessing a given font set,
            - The ttf font filename,
            - The json charmap filename,
            - Optionally, the directory containing these files. When not
              provided, the files will be looked for in ``./fonts/``.
        """
        super(IconicFont, self).__init__()
        self.painter = CharIconPainter()
        self.painters = {}
        self.fontname = {}
        self.charmap = {}
        for fargs in args:
            self.loadFont(*fargs)

    def loadFont(self, prefix, ttfFilename, charmapFilename, directory=None):
        """Loads a font file and the associated charmap.

        If ``directory`` is None, the files will be looked for in ``./fonts/``.

        Parameters
        ----------
        prefix: str
            Prefix string to be used when accessing a given font set
        ttfFilename: str
            Ttf font filename
        charmapFilename: str
            Charmap filename
        directory: str or None, optional
            Directory for font and charmap files
        """

        def hook(obj):
            result = {}
            for key in obj:
                result[key] = unichr(int(obj[key], 16))
            return result

        if directory is None:
            directory = getDefaultFontDirectory()

        with open(os.path.join(directory, charmapFilename), 'r') as codes:
            self.charmap[prefix] = json.load(codes, object_hook=hook)

        id_ = QtGui.QFontDatabase.addApplicationFont(os.path.join(directory, ttfFilename))

        loadedFontFamilies = QtGui.QFontDatabase.applicationFontFamilies(id_)

        if (loadedFontFamilies):
            self.fontname[prefix] = loadedFontFamilies[0]
        else:
            print('Font is empty')

    def icon(self, *names, **kwargs):
        """
        Return a QtGui.QIcon object corresponding to the provided icon name.
        """
        optionsList = kwargs.pop('options', [{}] * len(names))
        generalOptions = kwargs

        if len(optionsList) != len(names):
            error = '"options" must be a list of size {0}'.format(len(names))
            raise Exception(error)

        parsedOptions = []
        for i in range(len(optionsList)):
            specificOptions = optionsList[i]
            parsedOptions.append(self._parseOptions(specificOptions,
                                                    generalOptions,
                                                    names[i]))

        # Process high level API
        apiOptions = parsedOptions

        return self._iconByPainter(self.painter, apiOptions)

    def _parseOptions(self, specificOptions, generalOptions, name):
        options = dict(_defaultOptions, **generalOptions)
        options.update(specificOptions)

        # Handle icons for modes (Active, Disabled, Selected, Normal)
        # and states (On, Off)
        iconKW = ['char', 'on', 'off', 'active', 'selected', 'disabled',
                  'onActive', 'onSelected', 'onDisabled', 'offActive',
                  'offSelected', 'offDisabled']
        char = options.get('char', name)
        on = options.get('on', char)
        off = options.get('off', char)
        active = options.get('active', on)
        selected = options.get('selected', active)
        disabled = options.get('disabled', char)
        onActive = options.get('onActive', active)
        onSelected = options.get('onSelected', selected)
        onDisabled = options.get('onDisabled', disabled)
        offActive = options.get('offActive', active)
        offSelected = options.get('offSelected', selected)
        offDisabled = options.get('offDisabled', disabled)

        iconDict = {'char': char,
                    'on': on,
                    'off': off,
                    'active': active,
                    'selected': selected,
                    'disabled': disabled,
                    'onActive': onActive,
                    'onSelected': onSelected,
                    'onDisabled': onDisabled,
                    'offActive': offActive,
                    'offSelected': offSelected,
                    'offDisabled': offDisabled,
                    }
        names = [iconDict.get(kw, name) for kw in iconKW]
        prefix, chars = self._getPrefixChars(names)
        options.update(dict(zip(*(iconKW, chars))))
        options.update({'prefix': prefix})

        # Handle colors for modes (Active, Disabled, Selected, Normal)
        # and states (On, Off)
        color = options.get('color')
        options.setdefault('colorOn', color)
        options.setdefault('colorActive', options['colorOn'])
        options.setdefault('colorSelected', options['colorActive'])
        options.setdefault('colorOnActive', options['colorActive'])
        options.setdefault('colorOnSelected', options['colorSelected'])
        options.setdefault('colorOnDisabled', options['colorDisabled'])
        options.setdefault('colorOff', color)
        options.setdefault('colorOffActive', options['colorActive'])
        options.setdefault('colorOffSelected', options['colorSelected'])
        options.setdefault('colorOffDisabled', options['colorDisabled'])

        return options

    def _getPrefixChars(self, names):
        chars = []
        for name in names:
            if '.' in name:
                prefix, n = name.split('.')
                if prefix in self.charmap:
                    if n in self.charmap[prefix]:
                        chars.append(self.charmap[prefix][n])
                    else:
                        error = 'Invalid icon name "{0}" in font "{1}"'.format(
                            n, prefix)
                        raise Exception(error)
                else:
                    error = 'Invalid font prefix "{0}"'.format(prefix)
                    raise Exception(error)
            else:
                raise Exception('Invalid icon name')

        return prefix, chars

    def font(self, prefix, size):
        """Return a QtGui.QFont corresponding to the given prefix and size."""
        font = QtGui.QFont(self.fontname[prefix])
        font.setPixelSize(size)
        return font

    def setCustomIcon(self, name, painter):
        """Associate a user-provided CharIconPainter to an icon name.

        The custom icon can later be addressed by calling
        icon('custom.NAME') where NAME is the provided name for that icon.

        Parameters
        ----------
        name: str
            name of the custom icon
        painter: CharIconPainter
            The icon painter, implementing
            ``paint(self, iconic, painter, rect, mode, state, options)``
        """
        self.painters[name] = painter

    def _customIcon(self, name, **kwargs):
        """Return the custom icon corresponding to the given name."""
        options = dict(_defaultOptions, **kwargs)
        if name in self.painters:
            painter = self.painters[name]
            return self._iconByPainter(painter, options)
        else:
            return QtGui.QIcon()

    def _iconByPainter(self, painter, options):
        """Return the icon corresponding to the given painter."""
        engine = CharIconEngine(self, painter, options)
        return QtGui.QIcon(engine)
