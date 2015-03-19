"""Classes handling iconic fonts"""

from __future__ import print_function

import json
import os

from qtpy.QtCore import Qt, QObject, QPoint, QRect, qRound, QByteArray
from qtpy.QtGui import QIcon, QColor, QIconEngine, QPainter, QPixmap, \
    QFontDatabase, QFont
from six import unichr


_default_options = {
    'color': QColor(50, 50, 50),
    'scale_factor': 0.9,
}


class CharIconPainter:

    """Char icon painter"""

    def paint(self, awesome, painter, rect, mode, state, options):
        """Main paint method"""
        if isinstance(options, list):
            for opt in options:
                self._paint_icon(awesome, painter, rect, mode, state, opt)
        else:
            self._paint_icon(awesome, painter, rect, mode, state, options)

    def _paint_icon(self, awesome, painter, rect, mode, state, options):
        """Paint a single icon"""
        painter.save()
        color, char = options['color'], options['char']

        if mode == QIcon.Disabled:
            color = options.get('color_disabled', color)
            char = options.get('disabled', char)
        elif mode == QIcon.Active:
            color = options.get('color_active', color)
            char = options.get('active', char)
        elif mode == QIcon.Selected:
            color = options.get('color_selected', color)
            char = options.get('selected', char)

        painter.setPen(QColor(color))

        draw_size = qRound(rect.height() * options['scale_factor'])
        prefix = options['prefix']

        # Animation setup hook
        animation = options.get('animation')
        if animation is not None:
            animation.setup(self, painter, rect)

        painter.setFont(awesome.font(prefix, draw_size))
        if 'offset' in options:
            rect = QRect(rect)
            rect.translate(options['offset'][0] * rect.width(),
                           options['offset'][1] * rect.height())

        painter.setOpacity(options.get('opacity', 1.0))

        painter.drawText(rect, Qt.AlignCenter | Qt.AlignVCenter, char)
        painter.restore()


class CharIconEngine(QIconEngine):

    """Icon engine"""

    def __init__(self, awesome, painter, options):
        super(CharIconEngine, self).__init__()
        self.awesome = awesome
        self.painter = painter
        self.options = options

    def paint(self, painter, rect, mode, state):
        self.painter.paint(
            self.awesome, painter, rect, mode, state, self.options)

    def pixmap(self, size, mode, state):
        pm = QPixmap(size)
        pm.fill(Qt.transparent)
        self.paint(QPainter(pm), QRect(QPoint(0, 0), size), mode, state)
        return pm


class IconicFont(QObject):

    """Main class for managing iconic fonts"""

    def __init__(self, *args):
        """Constructor

        Arguments
        ---------
        *args: tuples
            Each positional argument is a tuple of 3 or 4 values
            - The prefix string to be used when accessing a given font set
            - The ttf font filename
            - The json charmap filename
            - Optionally, the directory containing these files. When not
              provided, the files will be looked up in ./fonts/
        """
        super(IconicFont, self).__init__()
        self.painter = CharIconPainter()
        self.painters = {}
        self.fontname = {}
        self.charmap = {}
        for fargs in args:
            self.load_font(*fargs)

    def load_font(self, prefix, ttf_filename, charmap_filename, directory=None):
        """Loads a font file and the associated charmap

        If `directory` is None, the files will be looked up in ./fonts/

        Arguments
        ---------
        prefix: str
            prefix string to be used when accessing a given font set
        ttf_filename: str
            ttf font filename
        charmap_filename: str
            charmap filename
        directory: str or None, optional
            directory for font and charmap files
        """

        def hook(obj):
            result = {}
            for key in obj:
                result[key] = unichr(int(obj[key], 16))
            return result

        if directory is None:
            directory = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'fonts')
        with open(os.path.join(directory, ttf_filename), 'rb') as f:
            font_data = QByteArray(f.read())
        with open(os.path.join(directory, charmap_filename), 'r') as codes:
            self.charmap[prefix] = json.load(codes, object_hook=hook)
        id_ = QFontDatabase.addApplicationFontFromData(font_data)
        loadedFontFamilies = QFontDatabase.applicationFontFamilies(id_)
        if(loadedFontFamilies):
            self.fontname[prefix] = loadedFontFamilies[0]
        else:
            print('Font is empty')

    def icon(self, name, **kwargs):
        """Returns a QIcon object corresponding to the provided icon name
        (including prefix)

        Arguments
        ---------
        fullname: str
            icon name, of the form PREFIX.NAME
        options: dict or None
            options to be passed to the icon painter
        """
        prefix, name = name.split('.')
        if prefix == 'custom':
            return self._custom_icon(name, **kwargs)
        else:
            for kw in ['disabled', 'active', 'selected']:
                if kw in kwargs:
                    p, n = kwargs[kw].split('.')
                    if n in self.charmap[p]:
                        kwargs[kw] = self.charmap[p][n]
            options = dict(_default_options, **kwargs)
            if name in self.charmap[prefix]:
                options = dict(
                    options, char=self.charmap[prefix][name], prefix=prefix,)
            return self._icon_by_painter(self.painter, options)

    def icon_stack(self, names, options=None):
        """Returns a QIcon object corresponding to the provided icon names
        (including prefixes)

        Arguments
        ---------
        names: list of str
            icon names, of the form PREFIX.NAME
        options: list of dict or None
            options to be passed to the icon painter
        """
        prefixes, names = zip(*(fn.split('.') for fn in names))
        chars = [self.charmap[p][n] for p, n in zip(prefixes, names)]
        if options is None:
            options = [{}] * len(chars)
        elif isinstance(options, dict):
            options = [options] * len(chars)
        for kwargs in options:
            for kw in ['disabled', 'active', 'selected']:
                if kw in kwargs:
                    p, n = kwargs[kw].split('.')
                    if n in self.charmap[p]:
                        kwargs[kw] = self.charmap[p][n]
        options = [dict(_default_options, prefix=prefixes[i], char=chars[i],
                        **(options[i])) for i in range(len(chars))]
        return self._icon_by_painter(self.painter, options)

    def font(self, prefix, size):
        """Returns QFont corresponding to the given prefix and size

        Arguments
        ---------
        prefix: str
            prefix string of the loaded font
        size: int
            size for the font
        """
        font = QFont(self.fontname[prefix])
        font.setPixelSize(size)
        return font

    def set_custom_icon(self, name, painter):
        """Associates a user-provided CharIconPainter to an icon name
        The custom icon can later be addressed by calling
        icon('custom.NAME') where NAME is the provided name for that icon.

        Arguments
        ---------
        name: str
            name of the custom icon
        painter: CharIconPainter
            The icon painter, implementing
            `paint(self, awesome, painter, rect, mode, state, options)`
        """
        self.painters[name] = painter

    def _custom_icon(self, name, **kwargs):
        """Returns the custom icon corresponding to the given name"""
        options = dict(_default_options, **kwargs)
        if name in self.painters:
            painter = self.painters[name]
            return self._icon_by_painter(painter, options)
        else:
            return QIcon()

    def _icon_by_painter(self, painter, options):
        """Returns the icon corresponding to the given painter"""
        engine = CharIconEngine(self, painter, options)
        return QIcon(engine)
