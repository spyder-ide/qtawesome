#!/usr/bin/env python
"""Test script for all qtawesome animations."""

import sys
from qtpy import QtWidgets, QtCore
import qtawesome as qta


class AnimationTestWindow(QtWidgets.QWidget):
    """Window to test all animation types."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("QtAwesome Animation Test")
        self.setMinimumSize(600, 500)

        layout = QtWidgets.QVBoxLayout()

        # Title
        title = QtWidgets.QLabel("QtAwesome Animation Test Suite")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        # Create grid for animations
        grid = QtWidgets.QGridLayout()

        # Spin animation
        spin_button = QtWidgets.QPushButton("  Spin (continuous rotation)")
        spin_anim = qta.Spin(spin_button)
        spin_icon = qta.icon("fa5s.spinner", color="blue", animation=spin_anim)
        spin_button.setIcon(spin_icon)
        spin_button.setIconSize(QtCore.QSize(32, 32))
        grid.addWidget(spin_button, 0, 0)

        # Pulse animation
        pulse_button = QtWidgets.QPushButton("  Pulse (45° steps)")
        pulse_anim = qta.Pulse(pulse_button)
        pulse_icon = qta.icon("fa5s.spinner", color="green", animation=pulse_anim)
        pulse_button.setIcon(pulse_icon)
        pulse_button.setIconSize(QtCore.QSize(32, 32))
        grid.addWidget(pulse_button, 0, 1)

        # Breathe animation
        breathe_button = QtWidgets.QPushButton("  Breathe (scale)")
        breathe_anim = qta.Breathe(breathe_button)
        breathe_icon = qta.icon("fa5s.heart", color="red", animation=breathe_anim)
        breathe_button.setIcon(breathe_icon)
        breathe_button.setIconSize(QtCore.QSize(32, 32))
        grid.addWidget(breathe_button, 1, 0)

        # Fade animation
        fade_button = QtWidgets.QPushButton("  Fade (opacity)")
        fade_anim = qta.Fade(fade_button)
        fade_icon = qta.icon("fa5s.lightbulb", color="orange", animation=fade_anim)
        fade_button.setIcon(fade_icon)
        fade_button.setIconSize(QtCore.QSize(32, 32))
        grid.addWidget(fade_button, 1, 1)

        # Shake animation
        shake_button = QtWidgets.QPushButton("  Shake (vibrate)")
        shake_anim = qta.Shake(shake_button, amplitude_x=2, amplitude_y=2)
        shake_icon = qta.icon("fa5s.bell", color="purple", animation=shake_anim)
        shake_button.setIcon(shake_icon)
        shake_button.setIconSize(QtCore.QSize(32, 32))
        grid.addWidget(shake_button, 2, 0)

        # ColorCycle animation
        color_button = QtWidgets.QPushButton("  ColorCycle (rainbow)")
        color_anim = qta.ColorCycle(color_button)
        color_icon = qta.icon("fa5s.star", animation=color_anim)
        color_button.setIcon(color_icon)
        color_button.setIconSize(QtCore.QSize(32, 32))
        grid.addWidget(color_button, 2, 1)

        # Spin with duration
        spin_duration_button = QtWidgets.QPushButton("  Spin (5s duration)")
        spin_duration_anim = qta.Spin(spin_duration_button, duration=5000)
        spin_duration_icon = qta.icon(
            "fa5s.hourglass", color="brown", animation=spin_duration_anim
        )
        spin_duration_button.setIcon(spin_duration_icon)
        spin_duration_button.setIconSize(QtCore.QSize(32, 32))
        grid.addWidget(spin_duration_button, 3, 0)

        # Breathe with custom params
        breathe_fast_button = QtWidgets.QPushButton("  Breathe (fast, large)")
        breathe_fast_anim = qta.Breathe(
            breathe_fast_button, interval=10, min_scale=0.5, max_scale=1.5
        )
        breathe_fast_icon = qta.icon(
            "fa5s.circle", color="cyan", animation=breathe_fast_anim
        )
        breathe_fast_button.setIcon(breathe_fast_icon)
        breathe_fast_button.setIconSize(QtCore.QSize(32, 32))
        grid.addWidget(breathe_fast_button, 3, 1)

        layout.addLayout(grid)

        # Control buttons
        control_layout = QtWidgets.QHBoxLayout()

        # Start/Stop manual control
        manual_control_label = QtWidgets.QLabel("Manual Control:")
        control_layout.addWidget(manual_control_label)

        self.manual_button = QtWidgets.QPushButton("  Manual")
        self.manual_anim = qta.Spin(self.manual_button, autostart=False)
        manual_icon = qta.icon("fa5s.cog", color="gray", animation=self.manual_anim)
        self.manual_button.setIcon(manual_icon)
        self.manual_button.setIconSize(QtCore.QSize(32, 32))
        control_layout.addWidget(self.manual_button)

        start_btn = QtWidgets.QPushButton("Start")
        start_btn.clicked.connect(self.manual_anim.start)
        control_layout.addWidget(start_btn)

        stop_btn = QtWidgets.QPushButton("Stop")
        stop_btn.clicked.connect(self.manual_anim.stop)
        control_layout.addWidget(stop_btn)

        reset_btn = QtWidgets.QPushButton("Reset")
        reset_btn.clicked.connect(self.manual_anim.reset)
        control_layout.addWidget(reset_btn)

        control_layout.addStretch()

        layout.addLayout(control_layout)

        # Info section
        info = QtWidgets.QLabel(
            "Test all animation types:\n"
            "• Spin: Continuous smooth rotation\n"
            "• Pulse: Stepped 45° rotation\n"
            "• Breathe: Scaling effect (grows/shrinks)\n"
            "• Fade: Opacity pulsating\n"
            "• Shake: Vibration/bounce effect\n"
            "• ColorCycle: Cycles through rainbow colors\n"
            "• Duration: Animations can have limited duration\n"
            "• Manual: Control animations with start/stop/reset"
        )
        info.setStyleSheet(
            "margin: 10px; padding: 10px; background-color: #000000; border-radius: 5px;"
        )
        layout.addWidget(info)

        self.setLayout(layout)


def main():
    """Run the animation test application."""
    app = QtWidgets.QApplication(sys.argv)
    window = AnimationTestWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
