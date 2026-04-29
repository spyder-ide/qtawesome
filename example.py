# -*- coding: utf-8 -*-

# Standard library imports
import sys

# Third party imports
from qtpy import QtCore, QtWidgets

# Local imports
import qtawesome as qta


ICON_SIZE = QtCore.QSize(28, 28)


class AwesomeExample(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(qta.icon("fa5s.icons"))

        # Label for supported fonts
        supported_fonts_label = QtWidgets.QLabel("Supported fonts (prefix)")
        supported_fonts_label.setAlignment(QtCore.Qt.AlignCenter)

        # Get FontAwesome 6.x icons by name in various styles:
        fa6_icon = qta.icon("fa6.flag")
        fa6_button = QtWidgets.QPushButton(fa6_icon, "Font Awesome 6! (regular)")

        fa6s_icon = qta.icon("fa6s.flag")
        fa6s_button = QtWidgets.QPushButton(fa6s_icon, "Font Awesome 6! (solid)")

        fa6b_icon = qta.icon("fa6b.github")
        fa6b_button = QtWidgets.QPushButton(fa6b_icon, "Font Awesome 6! (brands)")

        # Get FontAwesome 5.x icons by name in various styles:
        fa5_icon = qta.icon("fa5.flag")
        fa5_button = QtWidgets.QPushButton(fa5_icon, "Font Awesome 5! (regular)")

        fa5s_icon = qta.icon("fa5s.flag")
        fa5s_button = QtWidgets.QPushButton(fa5s_icon, "Font Awesome 5! (solid)")

        fa5b_icon = qta.icon("fa5b.github")
        fa5b_button = QtWidgets.QPushButton(fa5b_icon, "Font Awesome 5! (brands)")

        # Get Elusive icons by name
        asl_icon = qta.icon("ei.asl")
        elusive_button = QtWidgets.QPushButton(asl_icon, "Elusive Icons (ei)")

        # Get Material Design icons by name
        apn_icon = qta.icon("mdi6.access-point-network")
        mdi6_button = QtWidgets.QPushButton(apn_icon, "Material Design (mdi, mdi6)")

        # Get Phosphor by name
        mic_icon = qta.icon("ph.microphone-fill")
        ph_button = QtWidgets.QPushButton(mic_icon, "Phosphor Icons (ph)")

        # Get Remix Icon by name
        truck_icon = qta.icon("ri.truck-fill")
        ri_button = QtWidgets.QPushButton(truck_icon, "Remix Icons (ri)")

        # Get Microsoft's Codicons by name
        squirrel_icon = qta.icon("msc.squirrel")
        msc_button = QtWidgets.QPushButton(squirrel_icon, "Codicons (msc)")

        # Label for style options
        styles_label = QtWidgets.QLabel("Styles")
        styles_label.setAlignment(QtCore.Qt.AlignCenter)

        # Label for animations
        animations_label = QtWidgets.QLabel("Animations")
        animations_label.setAlignment(QtCore.Qt.AlignCenter)

        # Rotated
        rot_icon = qta.icon("mdi.access-point-network", rotated=45)
        rot_button = QtWidgets.QPushButton(rot_icon, "Rotated Icons")

        # Horizontal flip
        hflip_icon = qta.icon("mdi.account-alert", hflip=True)
        hflip_button = QtWidgets.QPushButton(hflip_icon, "Horizontally Flipped Icons")

        # Vertical flip
        vflip_icon = qta.icon("mdi.account-alert", vflip=True)
        vflip_button = QtWidgets.QPushButton(vflip_icon, "Vertically Flipped Icons")

        # Styling
        styling_icon = qta.icon(
            "fa5s.music",
            active="fa5s.balance-scale",
            color="blue",
            color_active="orange",
        )
        music_button = QtWidgets.QPushButton(styling_icon, "Changing colors")

        # Setting an alpha of 165 to the color of this icon. Alpha must be a number
        # between 0 and 255.
        icon_with_alpha = qta.icon("mdi.heart", color=("red", 120))
        heart_button = QtWidgets.QPushButton(icon_with_alpha, "Setting alpha")

        # Toggle
        toggle_icon = qta.icon(
            "fa5s.home",
            selected="fa5s.balance-scale",
            color_off="black",
            color_off_active="blue",
            color_on="orange",
            color_on_active="yellow",
        )
        toggle_button = QtWidgets.QPushButton(toggle_icon, "Toggle")
        toggle_button.setCheckable(True)

        iconwidget = qta.IconWidget()
        spin_icon = qta.icon("mdi.loading", color="red", animation=qta.Spin(iconwidget))
        iconwidget.setIcon(spin_icon)
        iconwidget.setIconSize(ICON_SIZE)
        iconwidgetholder = QtWidgets.QWidget()
        lo = QtWidgets.QHBoxLayout()
        lo.addWidget(iconwidget)
        lo.addWidget(QtWidgets.QLabel("IconWidget"))
        iconwidgetholder.setLayout(lo)
        iconwidget2 = qta.IconWidget("mdi.web", color="blue", size=QtCore.QSize(16, 16))

        # Icon drawn with the `image` option
        drawn_image_icon = qta.icon("ri.truck-fill", options=[{"draw": "image"}])
        drawn_image_button = QtWidgets.QPushButton(
            drawn_image_icon, "Icon drawn as an image"
        )

        # Stack icons
        camera_ban = qta.icon(
            "fa5s.camera",
            "fa5s.ban",
            options=[
                {"scale_factor": 0.5, "active": "fa5s.balance-scale"},
                {"color": "red", "opacity": 0.7},
            ],
        )
        stack_button = QtWidgets.QPushButton(camera_ban, "Stack")
        stack_button.setIconSize(ICON_SIZE)

        # Stack and offset icons
        saveall = qta.icon(
            "fa5.save",
            "fa5.save",
            options=[
                {"scale_factor": 0.8, "offset": (0.2, 0.2), "color": "gray"},
                {"scale_factor": 0.8},
            ],
        )
        saveall_button = QtWidgets.QPushButton(saveall, "Stack, offset")

        # Spin icons
        spin_button = QtWidgets.QPushButton(" Spinning icon")
        animation1 = qta.Spin(spin_button)
        spin_icon = qta.icon("fa5s.spinner", color="red", animation=animation1)
        spin_button.setIcon(spin_icon)

        timer1 = QtCore.QTimer()
        timer1.singleShot(3000, animation1.stop)

        # Pulse icons
        pulse_button = QtWidgets.QPushButton(" Pulsing icon")
        animation2 = qta.Pulse(pulse_button, autostart=False)
        pulse_icon = qta.icon("fa5s.spinner", color="green", animation=animation2)
        pulse_button.setIcon(pulse_icon)

        timer2 = QtCore.QTimer()
        timer2.singleShot(1500, animation2.start)
        timer3 = QtCore.QTimer()
        timer3.singleShot(6000, animation2.stop)

        # Stacked spin icons
        stack_spin_button = QtWidgets.QPushButton("Stack spin")
        options = [
            {"scale_factor": 0.4, "animation": qta.Spin(stack_spin_button)},
            {"color": "blue"},
        ]
        stack_spin_icon = qta.icon("ei.asl", "fa5.square", options=options)
        stack_spin_button.setIcon(stack_spin_icon)
        stack_spin_button.setIconSize(ICON_SIZE)

        # Breathe animation
        breathe_button = QtWidgets.QPushButton(" Breathe")
        animation3 = qta.Breathe(breathe_button)
        breathe_icon = qta.icon("fa5s.heart", color="red", animation=animation3)
        breathe_button.setIcon(breathe_icon)
        breathe_button.setIconSize(ICON_SIZE)

        # Fade animation
        fade_button = QtWidgets.QPushButton(" Fade")
        animation4 = qta.Fade(fade_button)
        fade_icon = qta.icon("fa5s.lightbulb", color="orange", animation=animation4)
        fade_button.setIcon(fade_icon)
        fade_button.setIconSize(ICON_SIZE)

        # Shake animation
        shake_button = QtWidgets.QPushButton(" Shake")
        animation5 = qta.Shake(shake_button, amplitude_x=2, amplitude_y=2)
        shake_icon = qta.icon("fa5s.bell", color="purple", animation=animation5)
        shake_button.setIcon(shake_icon)
        shake_button.setIconSize(ICON_SIZE)

        # ColorCycle animation
        color_button = QtWidgets.QPushButton(" ColorCycle")
        animation6 = qta.ColorCycle(color_button)
        color_icon = qta.icon("fa5s.star", animation=animation6)
        color_button.setIcon(color_icon)
        color_button.setIconSize(ICON_SIZE)

        # HeartBeat animation
        heartbeat_button = QtWidgets.QPushButton(" HeartBeat")
        animation7 = qta.HeartBeat(heartbeat_button)
        heartbeat_icon = qta.icon("fa5s.heart", color="crimson", animation=animation7)
        heartbeat_button.setIcon(heartbeat_icon)
        heartbeat_button.setIconSize(ICON_SIZE)

        # Swing animation
        swing_button = QtWidgets.QPushButton(" Swing")
        animation8 = qta.Swing(swing_button, angle=20)
        swing_icon = qta.icon("fa5s.bell", color="gold", animation=animation8)
        swing_button.setIcon(swing_icon)
        swing_button.setIconSize(ICON_SIZE)

        # Elastic animation
        elastic_button = QtWidgets.QPushButton(" Elastic")
        animation9 = qta.Elastic(elastic_button, min_scale=0.6, max_scale=1.0)
        elastic_icon = qta.icon(
            "fa5s.certificate", color="purple", animation=animation9
        )
        elastic_button.setIcon(elastic_icon)
        elastic_button.setIconSize(ICON_SIZE)

        # Composite animation (Spin + Breathe)
        composite_button = QtWidgets.QPushButton(" Spin + Breathe")
        anim_spin = qta.Spin(composite_button, step=2, autostart=False)
        anim_breathe = qta.Breathe(
            composite_button, min_scale=0.8, max_scale=1.2, autostart=False
        )
        composite_anim = qta.CompositeAnimation(
            composite_button, [anim_spin, anim_breathe]
        )
        composite_icon = qta.icon("fa5s.star", color="orange", animation=composite_anim)
        composite_button.setIcon(composite_icon)
        composite_button.setIconSize(ICON_SIZE)

        # Render a label with this font
        label = QtWidgets.QLabel(chr(0xF19C) + " " + "Label")
        label.setFont(qta.font("fa5s", 16))

        # Layout
        grid = QtWidgets.QGridLayout()
        fonts_widgets = [
            supported_fonts_label,
            fa6_button,
            fa6s_button,
            fa6b_button,
            fa5_button,
            fa5s_button,
            fa5b_button,
            elusive_button,
            mdi6_button,
            ph_button,
            ri_button,
            msc_button,
        ]
        styled_widgets = [
            styles_label,
            music_button,
            heart_button,
            rot_button,
            hflip_button,
            vflip_button,
            toggle_button,
            drawn_image_button,
            stack_button,
            saveall_button,
        ]
        other_widgets = [label, iconwidget2]
        animated_widgets = [
            animations_label,
            spin_button,
            pulse_button,
            stack_spin_button,
            breathe_button,
            fade_button,
            shake_button,
            color_button,
            heartbeat_button,
            swing_button,
            elastic_button,
            composite_button,
            iconwidgetholder,
        ]

        for idx, w in enumerate(fonts_widgets):
            grid.addWidget(w, idx, 0)

        for idx, w in enumerate(styled_widgets):
            grid.addWidget(w, idx, 1)

        for idx, w in enumerate(other_widgets):
            grid.addWidget(w, idx + len(styled_widgets), 1)

        for idx, w in enumerate(animated_widgets):
            grid.addWidget(w, idx, 2)

        title = "Awesome"
        args = " ".join(sys.argv[1:]).strip()
        if args:
            title += " (" + args + ")"

        self.setLayout(grid)
        self.setWindowTitle(title)
        self.setMinimumWidth(720)
        self.show()


def main():
    global_defaults = {}
    for arg in sys.argv[1:]:
        try:
            key, val = arg.split("=", maxsplit=1)
            global_defaults[key] = val
        except Exception:
            pass
    if global_defaults:
        qta.set_global_defaults(**global_defaults)

    app = QtWidgets.QApplication(sys.argv)

    # Enable High DPI display with PyQt5
    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    # Timer needed to close the example application
    # when testing
    QtCore.QTimer.singleShot(10000, app.exit)
    _ = AwesomeExample()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
