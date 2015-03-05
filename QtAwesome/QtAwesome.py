from __future__ import print_function
from PyQt4.QtCore import Qt, QPoint, QRect, qRound
from PyQt4.QtGui import QIcon, QIconEngine, QPainter, QPixmap


class CharIconPainter: 
    """The char icon painter"""

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


from PyQt4.QtCore import QChar, QObject, QByteArray
from PyQt4.QtGui import QColor, QFontDatabase, QIcon, QFont
import os


_default_options = {
    'color' : QColor(50, 50, 50),
    'color-disabled' : QColor(70, 70, 70, 60),
    'color-active' : QColor(10, 10, 10),
    'color-selected' : QColor(10, 10, 10),
    'scale-factor' : 0.9,
}


class FontIconSet(QObject):
    """The main class for managing icons"""
    
    def __init__(self, ttf_filename, codes):
        """Takes a filename for the ttf font and a dictionary mapping icon
        names to char numbers"""
        super(FontIconSet, self).__init__()
        self.painter = CharIconPainter()
        self.codes = codes
        self.painters = {}
        self.ttf_name = ttf_filename
        self._load_font()

    def _load_font(self):
        """loads the font file"""
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            'fonts', self.ttf_name)
        with open(path, 'r') as file:
            font_data = QByteArray(file.read())
        
        id = QFontDatabase.addApplicationFontFromData(font_data)
        loadedFontFamilies = QFontDatabase.applicationFontFamilies(id)
        if(loadedFontFamilies):
            self.fontname = loadedFontFamilies[0]
        else:
            print('Font is empty')

    def by_char(self, character, options=None):
        """Returns the icon corresponding to the given character"""
        if options is None:
            options = {}
        options = dict(_default_options, **options)
        options['text'] = QChar(int(character))
        return self.by_painter(self.painter, options)

    def by_name(self, name, options=None):
        """Returns the icon corresponding to the given name"""
        if name in self.codes:
            return self.by_char(self.codes[name], options)
        if name in self.painters:
            painter = self.painters[name]
            return self.by_painter(painter, options)     
        else:
            return QIcon()
    
    def by_painter(self, painter, options=None):
        """Returns the icon corresponding to the given painter"""
        if options is None:
            options = {}
        options = dict(_default_options, **options)
        engine = CharIconEngine(self, painter, options)
        return QIcon(engine)
    
    def give(self, name, painter):
        """Associates a user provided painter to an icon name"""
        self.painters[name] = painter
    
    def font(self, size):
        """Returns the icon QFont with the given size"""
        font = QFont(self.fontname)
        font.setPixelSize(size)
        return font
