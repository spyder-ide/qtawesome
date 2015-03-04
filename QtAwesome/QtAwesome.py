"""
PyQtAwesome - use font-awesome in PyQt / PySide applications

This is a port to Python of the C++ QtAwesome by Rick Blommers
"""

from __future__ import print_function
from PyQt4.QtCore import (Qt, QObject, QFile, QPoint, QRect, QChar, qRound,
                          QByteArray, QIODevice)
from PyQt4.QtGui import (QFontDatabase, QIcon, QIconEngine, QPainter, QColor,
                         QPixmap, QFont)
import os
from .fa import codes

_default_options = {
    'color': QColor(50, 50, 50),
    'color-disabled': QColor(70, 70, 70, 60),
    'color-active': QColor(10, 10, 10),
    'color-selected': QColor(10, 10, 10),
    'scale-factor': 0.9,
}

_resource = { 'fontname' : None }

def _load():
    """Load the font file"""
    if(_resource['fontname'] is None):
        file = QFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  'fonts', 'fontawesome-4.3.0.ttf'))
        if(not file.open(QIODevice.ReadOnly)):
            print('Font awesome font could not be loaded')
            return False
        font_data = QByteArray(file.readAll())
        file.close()
        
        id = QFontDatabase.addApplicationFontFromData(font_data)
        loadedFontFamilies = QFontDatabase.applicationFontFamilies(id)
        if(loadedFontFamilies):
            _resource['fontname'] = loadedFontFamilies[0]
        else:
            print('Font is empty')
            return False
    return True


class QtAwesomeCharIconPainter: 
    """ The font-awesome icon painter"""

    def paint(self, awesome, painter, rect, mode, state, options):
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

        painter.setFont(awesome.font(drawSize))
        painter.drawText(rect, Qt.AlignCenter | Qt.AlignVCenter, text)
        painter.restore()


class QtAwesomeIconPainterIconEngine(QIconEngine):
    """ The painter icon engine. """

    def __init__(self, awesome, painter, options):
        super(QtAwesomeIconPainterIconEngine, self).__init__()
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


class QtAwesome(QObject):
    """The main class for managing icons"""
    
    def __init__(self):
        super(QtAwesome, self).__init__()
        self.painter = QtAwesomeCharIconPainter()
        self.painters = {}
        _load()

    def by_char(self, character, options={}):
        opt = dict(_default_options, **options)
        opt['text'] = QChar(int(character))
        return self.by_painter(self.painter, opt)

    def by_name(self, name, options={}):
        if name in codes:
            return self.by_char(codes[name], options)
        if name in self.painters:
            painter = self.painters[name]
            return self.by_painter(painter, options)     
        else:
            return QIcon()
    
    def by_painter(self, painter, options={}):
        opt = dict(_default_options, **options)
        engine = QtAwesomeIconPainterIconEngine(self, painter, opt)
        return QIcon(engine)
    
    def give(self, name, painter):
        self.painters[name] = painter
    
    def font(self, size):
        font = QFont(_resource['fontname'])
        font.setPixelSize(size)
        return font
