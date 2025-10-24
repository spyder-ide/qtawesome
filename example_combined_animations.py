#!/usr/bin/env python
"""Test script for new qtawesome animations including composite animations."""

import sys
from qtpy import QtWidgets, QtCore
import qtawesome as qta


class NewAnimationTestWindow(QtWidgets.QWidget):
    """Window to test new animation types and combinations."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("QtAwesome New Animations & Combinations")
        self.setMinimumSize(700, 600)

        layout = QtWidgets.QVBoxLayout()

        # Title
        title = QtWidgets.QLabel("New Animations & Combinations")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        # Create grid for animations
        grid = QtWidgets.QGridLayout()

        # Row 0: New single animations
        section1 = QtWidgets.QLabel("New Animations:")
        section1.setStyleSheet("font-weight: bold; margin-top: 10px;")
        grid.addWidget(section1, 0, 0, 1, 3)

        # HeartBeat animation
        heartbeat_button = QtWidgets.QPushButton("  HeartBeat")
        heartbeat_anim = qta.HeartBeat(heartbeat_button)
        heartbeat_icon = qta.icon("fa5s.heart", color="red", animation=heartbeat_anim)
        heartbeat_button.setIcon(heartbeat_icon)
        heartbeat_button.setIconSize(QtCore.QSize(32, 32))
        grid.addWidget(heartbeat_button, 1, 0)

        # Swing animation
        swing_button = QtWidgets.QPushButton("  Swing")
        swing_anim = qta.Swing(swing_button, angle=20)
        swing_icon = qta.icon("fa5s.bell", color="gold", animation=swing_anim)
        swing_button.setIcon(swing_icon)
        swing_button.setIconSize(QtCore.QSize(32, 32))
        grid.addWidget(swing_button, 1, 1)

        # Elastic animation
        elastic_button = QtWidgets.QPushButton("  Elastic")
        elastic_anim = qta.Elastic(elastic_button, min_scale=0.6, max_scale=1.0)
        elastic_icon = qta.icon("fa5s.certificate", color="purple", animation=elastic_anim)
        elastic_button.setIcon(elastic_icon)
        elastic_button.setIconSize(QtCore.QSize(32, 32))
        grid.addWidget(elastic_button, 1, 2)

        # Row 2: Composite animations
        section2 = QtWidgets.QLabel("Composite Animations (Combined Effects):")
        section2.setStyleSheet("font-weight: bold; margin-top: 20px;")
        grid.addWidget(section2, 2, 0, 1, 3)

        # Spin + Breathe
        spin_breathe_button = QtWidgets.QPushButton("  Spin + Breathe")
        anim1 = qta.Spin(spin_breathe_button, step=2, autostart=False)
        anim2 = qta.Breathe(spin_breathe_button, min_scale=0.8, max_scale=1.2, autostart=False)
        composite1 = qta.CompositeAnimation(spin_breathe_button, [anim1, anim2])
        composite1_icon = qta.icon("fa5s.star", color="orange", animation=composite1)
        spin_breathe_button.setIcon(composite1_icon)
        spin_breathe_button.setIconSize(QtCore.QSize(32, 32))
        grid.addWidget(spin_breathe_button, 3, 0)

        # Swing + Fade
        swing_fade_button = QtWidgets.QPushButton("  Swing + Fade")
        anim3 = qta.Swing(swing_fade_button, angle=25, autostart=False)
        anim4 = qta.Fade(swing_fade_button, min_opacity=0.3, autostart=False)
        composite2 = qta.CompositeAnimation(swing_fade_button, [anim3, anim4])
        composite2_icon = qta.icon("fa5s.moon", color="darkblue", animation=composite2)
        swing_fade_button.setIcon(composite2_icon)
        swing_fade_button.setIconSize(QtCore.QSize(32, 32))
        grid.addWidget(swing_fade_button, 3, 1)

        # Shake + ColorCycle
        shake_color_button = QtWidgets.QPushButton("  Shake + ColorCycle")
        anim5 = qta.Shake(shake_color_button, amplitude_x=2, amplitude_y=2, autostart=False)
        anim6 = qta.ColorCycle(shake_color_button, colors=['red', 'orange', 'yellow'], autostart=False)
        composite3 = qta.CompositeAnimation(shake_color_button, [anim5, anim6])
        composite3_icon = qta.icon("fa5s.fire", animation=composite3)
        shake_color_button.setIcon(composite3_icon)
        shake_color_button.setIconSize(QtCore.QSize(32, 32))
        grid.addWidget(shake_color_button, 3, 2)

        # HeartBeat + Fade
        heartbeat_fade_button = QtWidgets.QPushButton("  HeartBeat + Fade")
        anim7 = qta.HeartBeat(heartbeat_fade_button, max_scale=1.4, autostart=False)
        anim8 = qta.Fade(heartbeat_fade_button, min_opacity=0.4, autostart=False)
        composite4 = qta.CompositeAnimation(heartbeat_fade_button, [anim7, anim8])
        composite4_icon = qta.icon("fa5s.heartbeat", color="crimson", animation=composite4)
        heartbeat_fade_button.setIcon(composite4_icon)
        heartbeat_fade_button.setIconSize(QtCore.QSize(32, 32))
        grid.addWidget(heartbeat_fade_button, 4, 0)

        # Spin + Swing (double rotation effect)
        spin_swing_button = QtWidgets.QPushButton("  Spin + Swing")
        anim9 = qta.Spin(spin_swing_button, step=3, autostart=False)
        anim10 = qta.Swing(spin_swing_button, angle=10, autostart=False)
        composite5 = qta.CompositeAnimation(spin_swing_button, [anim9, anim10])
        composite5_icon = qta.icon("fa5s.compass", color="navy", animation=composite5)
        spin_swing_button.setIcon(composite5_icon)
        spin_swing_button.setIconSize(QtCore.QSize(32, 32))
        grid.addWidget(spin_swing_button, 4, 1)

        # Triple combo: Breathe + Swing + Fade
        triple_button = QtWidgets.QPushButton("  Breathe + Swing + Fade")
        anim11 = qta.Breathe(triple_button, min_scale=0.9, max_scale=1.1, autostart=False)
        anim12 = qta.Swing(triple_button, angle=15, autostart=False)
        anim13 = qta.Fade(triple_button, min_opacity=0.5, autostart=False)
        composite6 = qta.CompositeAnimation(triple_button, [anim11, anim12, anim13])
        composite6_icon = qta.icon("fa5s.gem", color="cyan", animation=composite6)
        triple_button.setIcon(composite6_icon)
        triple_button.setIconSize(QtCore.QSize(32, 32))
        grid.addWidget(triple_button, 4, 2)

        layout.addLayout(grid)

        # Comparison section
        section3 = QtWidgets.QLabel("Animation Variations:")
        section3.setStyleSheet("font-weight: bold; margin-top: 20px;")
        layout.addWidget(section3)

        var_grid = QtWidgets.QGridLayout()

        # HeartBeat variations
        hb1_button = QtWidgets.QPushButton("  Slow HeartBeat")
        hb1_anim = qta.HeartBeat(hb1_button, max_scale=1.2)
        hb1_anim.period = 1500  # Slower
        hb1_icon = qta.icon("fa5s.heart", color="pink", animation=hb1_anim)
        hb1_button.setIcon(hb1_icon)
        hb1_button.setIconSize(QtCore.QSize(28, 28))
        var_grid.addWidget(hb1_button, 0, 0)

        # Swing variations
        swing1_button = QtWidgets.QPushButton("  Wide Swing")
        swing1_anim = qta.Swing(swing1_button, angle=30)
        swing1_icon = qta.icon("fa5s.tag", color="green", animation=swing1_anim)
        swing1_button.setIcon(swing1_icon)
        swing1_button.setIconSize(QtCore.QSize(28, 28))
        var_grid.addWidget(swing1_button, 0, 1)

        # Elastic variations
        elastic1_button = QtWidgets.QPushButton("  Fast Elastic")
        elastic1_anim = qta.Elastic(elastic1_button, min_scale=0.3, max_scale=1.0)
        elastic1_anim.period = 800  # Faster
        elastic1_icon = qta.icon("fa5s.award", color="brown", animation=elastic1_anim)
        elastic1_button.setIcon(elastic1_icon)
        elastic1_button.setIconSize(QtCore.QSize(28, 28))
        var_grid.addWidget(elastic1_button, 0, 2)

        layout.addLayout(var_grid)

        # Info section
        info = QtWidgets.QLabel(
            "New Animations:\n"
            "• HeartBeat: Double pulse pattern with pause (lub-dub)\n"
            "• Swing: Pendulum-like rotation back and forth\n"
            "• Elastic: Spring-like bounce with overshoot\n\n"
            "Composite Animations:\n"
            "• Combine any animations together using CompositeAnimation\n"
            "• Example: Spin + Breathe creates a rotating, pulsing effect\n"
            "• Animations run simultaneously and blend their transformations\n\n"
            "Usage:\n"
            "  anim1 = qta.Spin(widget, autostart=False)\n"
            "  anim2 = qta.Breathe(widget, autostart=False)\n"
            "  composite = qta.CompositeAnimation(widget, [anim1, anim2])\n"
            "  icon = qta.icon('fa5s.star', animation=composite)"
        )
        info.setStyleSheet("margin: 10px; padding: 10px; background-color: #f0f0f0; border-radius: 5px; font-size: 11px;")
        layout.addWidget(info)

        self.setLayout(layout)


def main():
    """Run the new animation test application."""
    app = QtWidgets.QApplication(sys.argv)
    window = NewAnimationTestWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
