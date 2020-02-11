# -*- coding: utf-8 -*-

# Standard library imports
import sys

# Third party imports
from qtpy import QtCore, QtWidgets
from six import unichr

# Local imports
import qtawesome as qta


class AwesomeExample(QtWidgets.QDialog):

    def __init__(self):
        super(AwesomeExample, self).__init__()

        # Get FontAwesome 5.x icons by name in various styles by name
        fa5_icon = qta.icon('fa5.flag')
        fa5_button = QtWidgets.QPushButton(fa5_icon, 'Font Awesome! (regular)')

        fa5s_icon = qta.icon('fa5s.flag')
        fa5s_button = QtWidgets.QPushButton(fa5s_icon, 'Font Awesome! (solid)')

        fa5b_icon = qta.icon('fa5b.github')
        fa5b_button = QtWidgets.QPushButton(fa5b_icon, 'Font Awesome! (brands)')

        # Get Elusive icons by name
        asl_icon = qta.icon('ei.asl')
        elusive_button = QtWidgets.QPushButton(asl_icon, 'Elusive Icons!')

        # Get Material Design icons by name
        apn_icon = qta.icon('mdi.access-point-network')
        mdi_button = QtWidgets.QPushButton(apn_icon, 'Material Design Icons!')

        # Rotated
        rot_icon = qta.icon('mdi.access-point-network', rotated=45)
        rot_button = QtWidgets.QPushButton(rot_icon, 'Rotated Icons!')

        # Horizontal flip
        hflip_icon = qta.icon('mdi.account-alert', hflip=True)
        hflip_button = QtWidgets.QPushButton(hflip_icon, 'Horizontally Flipped Icons!')

        # Vertical flip
        vflip_icon = qta.icon('mdi.account-alert', vflip=True)
        vflip_button = QtWidgets.QPushButton(vflip_icon, 'Vertically Flipped Icons!')

        # Styling
        styling_icon = qta.icon('fa5s.music',
                                active='fa5s.balance-scale',
                                color='blue',
                                color_active='orange')
        music_button = QtWidgets.QPushButton(styling_icon, 'Styling')

        # Toggle
        toggle_icon = qta.icon('fa5s.home', selected='fa5s.balance-scale',
                               color_off='black',
                               color_off_active='blue',
                               color_on='orange',
                               color_on_active='yellow')
        toggle_button = QtWidgets.QPushButton(toggle_icon, 'Toggle')
        toggle_button.setCheckable(True)

        iconwidget = qta.IconWidget()
        spin_icon = qta.icon('mdi.loading', color='red',
                             animation=qta.Spin(iconwidget))
        iconwidget.setIcon(spin_icon)
        iconwidget.setIconSize(QtCore.QSize(32, 32))
        iconwidgetholder = QtWidgets.QWidget()
        lo = QtWidgets.QHBoxLayout()
        lo.addWidget(iconwidget)
        lo.addWidget(QtWidgets.QLabel('IconWidget'))
        iconwidgetholder.setLayout(lo)
        iconwidget2 = qta.IconWidget('mdi.web', color='blue')

        # Stack icons
        camera_ban = qta.icon('fa5s.camera', 'fa5s.ban',
                              options=[{'scale_factor': 0.5,
                                        'active': 'fa5s.balance-scale'},
                                       {'color': 'red', 'opacity': 0.7}])
        stack_button = QtWidgets.QPushButton(camera_ban, 'Stack')
        stack_button.setIconSize(QtCore.QSize(32, 32))

        # Stack and offset icons
        saveall = qta.icon('fa5.save', 'fa5.save',
                           options=[{'scale_factor': 0.8,
                                     'offset': (0.2, 0.2),
                                     'color': 'gray'},
                                    {'scale_factor': 0.8}])
        saveall_button = QtWidgets.QPushButton(saveall, 'Stack, offset')

        # Spin icons
        spin_button = QtWidgets.QPushButton(' Spinning icon')
        spin_icon = qta.icon('fa5s.spinner', color='red',
                             animation=qta.Spin(spin_button))
        spin_button.setIcon(spin_icon)

        # Pulse icons
        pulse_button = QtWidgets.QPushButton(' Pulsing icon')
        pulse_icon = qta.icon('fa5s.spinner', color='green',
                              animation=qta.Pulse(pulse_button))
        pulse_button.setIcon(pulse_icon)

        # Stacked spin icons
        stack_spin_button = QtWidgets.QPushButton('Stack spin')
        options = [{'scale_factor': 0.4,
                    'animation': qta.Spin(stack_spin_button)},
                   {'color': 'blue'}]
        stack_spin_icon = qta.icon('ei.asl', 'fa5.square',
                                   options=options)
        stack_spin_button.setIcon(stack_spin_icon)
        stack_spin_button.setIconSize(QtCore.QSize(32, 32))

        # Render a label with this font
        label = QtWidgets.QLabel(unichr(0xf19c) + ' ' + 'Label')
        label.setFont(qta.font('fa', 16))

        # Layout
        vbox = QtWidgets.QVBoxLayout()
        widgets = [
            fa5_button,
            fa5s_button,
            fa5b_button,
            elusive_button, 
            mdi_button,
            music_button,
            rot_button,
            hflip_button,
            vflip_button,
            toggle_button,
            stack_button,
            saveall_button,
            spin_button,
            pulse_button,
            stack_spin_button,
            label,
            iconwidgetholder,
            iconwidget2
        ]

        for w in widgets:
            vbox.addWidget(w)

        self.setLayout(vbox)
        self.setWindowTitle('Awesome')
        self.show()


def main():
    app = QtWidgets.QApplication(sys.argv)

    # Enable High DPI display with PyQt5
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    QtCore.QTimer.singleShot(10000, app.exit)
    _ = AwesomeExample()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
