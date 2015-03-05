"""
PyQtAwesome - use font-awesome in PyQt / PySide applications

This is a port to Python of the C++ QtAwesome by Rick Blommers
"""
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
