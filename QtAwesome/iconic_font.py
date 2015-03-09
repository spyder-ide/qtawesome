"""Classes handling iconic fonts"""

from __future__ import print_function
from PyQt4.QtCore import Qt, QObject, QChar, QPoint, QRect, qRound, QByteArray
from PyQt4.QtGui import (QIcon, QColor, QIconEngine, QPainter, QPixmap,
                         QFontDatabase, QFont)
import json
import os


class CharIconPainter: 
    """The char icon painter"""

    def paint(self, awesome, painter, rect, mode, state, options):
        # If options is a list, paint a stack of icons
        if isinstance(options, list):
            for opt in options:
                self.paint(awesome, painter, rect, mode, state, opt)
            return
        painter.save()
        color = options['color']
        text = options['text']
        
        if(mode == QIcon.Disabled):
            color = options['color-disabled']
            if 'text-disabled' in options: 
                text = options['text-disabled']
        elif (mode == QIcon.Active):
            color = options['color-active']
            if 'text-active' in options:
                text = options['text-active']
        elif(mode == QIcon.Selected):
            color = options['color-selected']
            if 'text-selected' in options: 
                text = options['text-selected']

        painter.setPen(color)

        drawSize = qRound(rect.height() * options['scale-factor'])
        prefix = options['prefix']

        painter.setFont(awesome.font(prefix, drawSize))
        painter.drawText(rect, Qt.AlignCenter | Qt.AlignVCenter, text)
        painter.restore()


class CharIconEngine(QIconEngine):
    """The painter icon engine"""

    def __init__(self, awesome, painter, options):
        super(CharIconEngine, self).__init__()
        self.awesome = awesome
        self.painter = painter
        self.options = options

    def paint(self, painter, rect, mode, state):
        self.painter.paint(self.awesome, painter, rect, mode, state, self.options)

    def pixmap(self, size, mode, state):
        pm = QPixmap(size)
        pm.fill(Qt.transparent)
        self.paint(QPainter(pm), QRect(QPoint(0, 0), size), mode, state)
        return pm


_default_options = {
    'color' : QColor(50, 50, 50),
    'color-disabled' : QColor(70, 70, 70, 60),
    'color-active' : QColor(10, 10, 10),
    'color-selected' : QColor(10, 10, 10),
    'scale-factor' : 0.9,
}


class IconicFont(QObject):
    """The main class for managing iconic fonts"""
    
    def __init__(self, *font_resources):
        """Takes a filename for the ttf font and a dictionary mapping icon
        names to char numbers"""
        super(IconicFont, self).__init__()
        self.painter = CharIconPainter()
        self.painters = {}
        self.fontname = {}
        self.charmap = {}
        for prefix, ttf_filename, charmap_filename in font_resources:
            self.load_font(prefix, ttf_filename, charmap_filename)

    def load_font(self, prefix, ttf_filename, charmap_filename):
        """loads the font file"""
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           'fonts', ttf_filename)
        with open(path, 'r') as file:
            font_data = QByteArray(file.read())

        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                    'fonts', charmap_filename)
        with open(path, 'r') as codes:
            self.charmap[prefix] = json.load(codes, object_hook=lambda o:{k : int(o[k], 16) for k in o})
        
        id = QFontDatabase.addApplicationFontFromData(font_data)
        loadedFontFamilies = QFontDatabase.applicationFontFamilies(id)
        if(loadedFontFamilies):
            self.fontname[prefix] = loadedFontFamilies[0]
        else:
            print('Font is empty')

    def icon(self, fullname, options=None):
        prefix, name = fullname.split('.')
        return self.icon_by_name(prefix, name, options)

    def icon_stack(self, fullnames, options=None):
        prefixes_names = zip(*(fn.split('.') for fn in fullnames))
        return self.icon_stack_by_name(*prefixes_names, options=options)

    def icon_by_name(self, prefix, name, options=None):
        """Returns the icon corresponding to the given name"""
        if prefix == 'custom':
            return self.custom_icon(name, options)
        if name in self.charmap[prefix]:
            return self.icon_by_char(prefix, self.charmap[prefix][name], options)
        else:
            return QIcon()

    def icon_stack_by_name(self, prefixes, names, options=None):
        """Returns the stacked icon corresponding to the given names""" 
        return self.icon_stack_by_char(prefixes, [self.charmap[p][n] for 
               p, n in zip(prefixes, names)], options)

    def custom_icon(self, name, options=None):
        """Returns the custom icon corresponding to the given name."""
        if options is None:
            options = {}
        if name in self.painters:
            painter = self.painters[name]
            return self._icon_by_painter(painter, options)     

    def icon_by_char(self, prefix, character, options=None):
        """Returns the icon corresponding to the given character"""
        if options is None:
            options = {}
        options = dict(_default_options, text=QChar(character), prefix=prefix,
                       **options)
        return self._icon_by_painter(self.painter, options)

    def icon_stack_by_char(self, prefixes, chars, options=None):
        """Returns the stacked icon corresponding to the given names"""
        if options is None:
            options = [{}] * len(chars)
        if isinstance(options, dict):
            options = [options] * len(chars)
        options = [dict(_default_options, prefix=prefixes[i], text=QChar(chars[i]),
                        **(options[i])) for i in xrange(len(chars))] 
        return self._icon_stack_by_painter(self.painter, options)

    def _icon_by_painter(self, painter, options):
        """Returns the icon corresponding to the given painter"""
        options = dict(_default_options, **options)
        engine = CharIconEngine(self, painter, options)
        return QIcon(engine)

    def _icon_stack_by_painter(self, painter, options):
        """Returns the icon stack corresponding to the given painter"""
        options = [dict(_default_options, **opt) for opt in options]
        engine = CharIconEngine(self, painter, options)
        return QIcon(engine)

    def set_custom_icon(self, name, painter):
        """Associates a user-provided CharIconPainter to an icon name"""
        self.painters[name] = painter

    def font(self, prefix, size):
        """Returns the icon QFont with the given size"""
        font = QFont(self.fontname[prefix])
        font.setPixelSize(size)
        return font
