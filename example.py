import sys
from qtpy import QtGui, QtCore
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
                                             {'color': 'red', 'opacity': 0.7}])
        stack_button = QtGui.QPushButton(camera_ban, 'Stack')
        stack_button.setIconSize(QtCore.QSize(32, 32))

        # Spin icons
        spin_button = QtGui.QPushButton(' Spinning icon')
        spin_icon = qta.icon('fa.spinner', color='red',
                             animation=qta.Spin(spin_button))
        spin_button.setIcon(spin_icon)

        # Pulse icons
        pulse_button = QtGui.QPushButton(' Pulsing icon')
        pulse_icon = qta.icon('fa.spinner', color='green',
                              animation=qta.Pulse(pulse_button))
        pulse_button.setIcon(pulse_icon)

        # Stacked spin icons
        stack_spin_button = QtGui.QPushButton('Stack spin')
        options = [{'scale_factor': 0.4,
                    'animation': qta.Spin(stack_spin_button)},
                   {'color': 'blue'}]
        stack_spin_icon = qta.icon_stack(['ei.asl', 'fa.squareo'],
                                         options=options)
        stack_spin_button.setIcon(stack_spin_icon)
        stack_spin_button.setIconSize(QtCore.QSize(32, 32))
        # Stack and offset icons
        saveall = qta.icon_stack(['fa.save', 'fa.save'],
                                   options=[{'scale_factor': 0.8, 
                                             'offset': (0.2, 0.2),
                                             'color': 'gray'},
                                            {'scale_factor': 0.8}])
        saveall_button = QtGui.QPushButton(saveall, 'Stack, offset')

        # Layout
        vbox = QtGui.QVBoxLayout()
        widgets = [fa_button, elusive_button, music_button, custom_button,
                   label, stack_button, saveall_button, spin_button, pulse_button,
                   stack_spin_button]
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
