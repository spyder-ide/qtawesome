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


class AwesomeExample(QtGui.QDialog):

    def __init__(self):
        super(AwesomeExample, self).__init__()

        # Get icons by name.
        fa_icon = qta.icon('fa.flag')
        fa_button = QtGui.QPushButton(fa_icon, 'Font Awesome!')

        asl_icon = qta.icon('ei.asl')
        elusive_button = QtGui.QPushButton(asl_icon, 'Elusive Icons!')

        # Styling
        styling_icon = qta.icon('fa.music',
                                active='fa.legal',
                                color='blue',
                                color_active='orange')
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
                                    options=[{'scale_factor': 0.5,
                                              'active': 'fa.legal'},
                                             {'color': 'red'}])
        stack_button = QtGui.QPushButton(camera_ban, 'Stack')
        stack_button.setIconSize(QtCore.QSize(32, 32))

        # Spin rotation icons
        spin_button = QtGui.QPushButton(' Spinning icon')
        spin_icon = qta.icon('fa.spinner', color='red', 
                             animation={'type': 'spin',
                                        'parent': spin_button})
        spin_button.setIcon(spin_icon)

        # Pulse rotation icons
        pulse_button = QtGui.QPushButton(' Pulsing icon')
        pulse_icon = qta.icon('fa.spinner', color='green',
                              animation={'type': 'pulse',
                                         'parent': pulse_button})
        pulse_button.setIcon(pulse_icon)

        # Stacked rotation icons
        stack_rotation_button = QtGui.QPushButton('Stack rotation')
        options = [{'scale_factor': 0.4,
                    'parent': stack_rotation_button,
                    'animation': {'type': 'spin',
                                  'parent': stack_rotation_button}
                    },
                   {'color': 'blue'}]
        stack_rotation_icon = qta.icon_stack(['ei.asl', 'fa.squareo'],
                                             options=options)
        stack_rotation_button.setIcon(stack_rotation_icon)
        stack_rotation_button.setIconSize(QtCore.QSize(32, 32))

        # Layout
        vbox = QtGui.QVBoxLayout()
        widgets = [fa_button, elusive_button, music_button, custom_button,
                   label, stack_button, spin_button, pulse_button,
                   stack_rotation_button]
        for w in widgets:
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
