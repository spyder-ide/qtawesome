import sys
from PyQt4 import QtGui, QtCore

from QtAwesome.QtAwesome import QtAwesome
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
        awesome = QtAwesome()
        
        # Call an icon by name
        beerButton = QtGui.QPushButton(awesome.by_name('beer'), 'Cheers!', self)
        
        # By Char, using the 'bunch' structure in fa
        coffeeButton = QtGui.QPushButton(awesome.by_char(fa.bunch.coffee),
                                         'Black please!', self)
        
        # Use some options
        musicButton = QtGui.QPushButton(awesome.by_name('music',
                                                        {'color': QtGui.QColor(255, 0, 0)}),
                                        'Music', self)
         
        # You can also directly render a label with this font
        label = QtGui.QLabel(QtCore.QChar(0xf0f4), self)
        
        # You can use a custom painter
        awesome.give("duplicate", DuplicateIconPainter())
        duplicateButton = QtGui.QPushButton(awesome.by_name('duplicate',
                                                            {'color': QtGui.QColor(255, 0, 0)}),
                                            'Custom painter', self)

        # Demo
        beerButton.move(50, 20)
        coffeeButton.move(50, 60)
        musicButton.move(50, 100) 
        label.move(50, 140)
        label.setFont(awesome.font(16))
        duplicateButton.move(50, 180) 
        
        self.setGeometry(300, 300, 250, 250)
        self.setWindowTitle('QtAwesome')
        self.show()


def main():    
    app = QtGui.QApplication(sys.argv)
    _ = AwesomeExample()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
