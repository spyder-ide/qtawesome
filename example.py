import sys
from PyQt4 import QtGui, QtCore
import QtAwesome as qta


class CustomIconPainter:

    """A custom painter for example bellow"""

    def paint(self, awesome, painter, rectIn, mode, state, options):
        drawSize = QtCore.qRound(rectIn.height() * 0.5)
        offset = rectIn.height() / 4.0
        char = qta.charmap('fa.plus')
        painter.setFont(awesome.font('fa', drawSize))
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

        # Get icons by name.
        fa_icon = qta.icon('fa.flag')
        fa_button = QtGui.QPushButton(fa_icon, 'Font Awesome!')

        asl_icon = qta.icon('ei.asl')
        elusive_button = QtGui.QPushButton(asl_icon, 'Elusive Icons!')

        # Styling
        styling_icon = qta.icon('fa.music',
                                {'color': QtGui.QColor(255, 0, 0),
                                 'color-active': QtGui.QColor(190, 0, 0)})
        music_button = QtGui.QPushButton(styling_icon, 'Styling')

        # Use a custom painter and assign it a name
        qta.set_custom_icon('double', CustomIconPainter())
        custom_button = QtGui.QPushButton(
            qta.icon('custom.double'), 'Custom painter')

        # Render a label with this font
        label = QtGui.QLabel(unichr(0xf19c) + ' ' + 'Label')
        label.setFont(qta.font('fa', 16))

        # Stack icons
        camera_ban = qta.icon_stack(['fa.camera', 'fa.ban'],
                                    options=[{'scale-factor': 0.5},
                                             {'color': QtGui.QColor(255, 0, 0)}])
        stack_button = QtGui.QPushButton(camera_ban, 'Stack')
        stack_button.setIconSize(QtCore.QSize(32, 32))

        # Layout
        vbox = QtGui.QVBoxLayout()
        for w in [fa_button, elusive_button, music_button, custom_button,
                  label, stack_button]:
            vbox.addWidget(w)

        self.setLayout(vbox)
        self.setWindowTitle('Awesome')
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    _ = AwesomeExample()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
