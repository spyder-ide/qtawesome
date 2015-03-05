import sys
from PyQt4 import QtGui, QtCore

from QtAwesome import fa


class DuplicateIconPainter:
    """A custom painter for example bellow"""
    def paint(self, awesome, painter, rectIn, mode, state, options):
        drawSize = QtCore.qRound(rectIn.height() * 0.5)
        offset = rectIn.height() / 4.0
        char = QtCore.QChar(fa.codes['plus'])
        painter.setFont(awesome.font(drawSize))
        painter.setPen(QtGui.QColor(100, 100, 100))
        painter.drawText(QtCore.QRect(QtCore.QPoint(offset * 2, offset * 2),
                                      QtCore.QSize(drawSize, drawSize)),
                         QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter, char)
        painter.setPen(QtGui.QColor(50, 50, 50))
        painter.drawText(QtCore.QRect(QtCore.QPoint(rectIn.width() - drawSize - offset,
                                                    rectIn.height() - drawSize - offset),
                                      QtCore.QSize(drawSize, drawSize)),
                         QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter, char)
        

class AwesomeExample(QtGui.QWidget):
    
    def __init__(self):
        super(AwesomeExample, self).__init__()
        
        # Call an icon by name
        beerButton = QtGui.QPushButton(fa.icon('beer'), 'Cheers!')
        
        coffeeButton = QtGui.QPushButton(fa.icon_by_char(fa.codes['coffee']), 'Black please!')
        
        # Pass options
        musicButton = QtGui.QPushButton(fa.icon('music', {'color': QtGui.QColor(255, 0, 0), 'verb' : 1}), 'Music')
         
        # You can also directly render a label with this font
        label = QtGui.QLabel(QtCore.QChar(0xf0f4))
        label.setFont(fa.font(16))

        # You can use a custom painter
        fa.give('double', DuplicateIconPainter())
        duplicateButton = QtGui.QPushButton(fa.icon('double'), 'Custom painter')

        # Layout
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(beerButton)
        vbox.addWidget(coffeeButton)
        vbox.addWidget(musicButton)
        vbox.addWidget(label)
        vbox.addWidget(duplicateButton)
        self.setLayout(vbox)
        self.setWindowTitle('Awesome')
        self.show()


def main():    
    app = QtGui.QApplication(sys.argv)
    _ = AwesomeExample()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

