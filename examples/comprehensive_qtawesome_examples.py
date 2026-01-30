"""
pip install pyside6 qtawesome thefuzz
"""

import sys
from thefuzz import fuzz
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QLabel,
    QGridLayout,
    QGroupBox,
    QPushButton,
    QSlider,
    QSpinBox,
    QComboBox,
    QScrollArea,
    QFrame,
    QToolButton,
    QCheckBox,
    QLineEdit,
    QDoubleSpinBox,
    QColorDialog,
    QSplitter,
    QMenu,
    QFileDialog,
    QInputDialog,
)
from PySide6.QtCore import Qt, QSize, QTimer, Signal
from PySide6.QtGui import QColor

import qtawesome as qta
from qtawesome.animation import Spin, Pulse


class FontShowcasePage(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)

        fonts_info = [
            (
                "fa5",
                "Font Awesome 5 Regular",
                [
                    "bookmark",
                    "bell",
                    "calendar",
                    "comment",
                    "envelope",
                    "file",
                    "heart",
                    "image",
                    "star",
                    "user",
                ],
            ),
            (
                "fa5s",
                "Font Awesome 5 Solid",
                [
                    "home",
                    "cog",
                    "check",
                    "times",
                    "search",
                    "plus",
                    "minus",
                    "trash",
                    "edit",
                    "save",
                ],
            ),
            (
                "fa5b",
                "Font Awesome 5 Brands",
                [
                    "github",
                    "twitter",
                    "facebook",
                    "google",
                    "apple",
                    "windows",
                    "linux",
                    "python",
                    "js",
                    "css3",
                ],
            ),
            (
                "fa6",
                "Font Awesome 6 Regular",
                [
                    "bookmark",
                    "bell",
                    "calendar",
                    "comment",
                    "envelope",
                    "file",
                    "heart",
                    "image",
                    "star",
                    "user",
                ],
            ),
            (
                "fa6s",
                "Font Awesome 6 Solid",
                [
                    "house",
                    "gear",
                    "check",
                    "xmark",
                    "magnifying-glass",
                    "plus",
                    "minus",
                    "trash",
                    "pen",
                    "floppy-disk",
                ],
            ),
            (
                "fa6b",
                "Font Awesome 6 Brands",
                [
                    "github",
                    "twitter",
                    "facebook",
                    "google",
                    "apple",
                    "windows",
                    "linux",
                    "python",
                    "js",
                    "css3",
                ],
            ),
            (
                "ei",
                "Elusive Icons",
                [
                    "home",
                    "cog",
                    "ok",
                    "remove",
                    "search",
                    "plus",
                    "minus",
                    "trash",
                    "pencil",
                    "file",
                ],
            ),
            (
                "mdi",
                "Material Design Icons 5",
                [
                    "home",
                    "cog",
                    "check",
                    "close",
                    "magnify",
                    "plus",
                    "minus",
                    "delete",
                    "pencil",
                    "content-save",
                ],
            ),
            (
                "mdi6",
                "Material Design Icons 6",
                [
                    "home",
                    "cog",
                    "check",
                    "close",
                    "magnify",
                    "plus",
                    "minus",
                    "delete",
                    "pencil",
                    "content-save",
                ],
            ),
            (
                "ph",
                "Phosphor Icons",
                [
                    "house",
                    "gear",
                    "check",
                    "x",
                    "magnifying-glass",
                    "plus",
                    "minus",
                    "trash",
                    "pencil",
                    "floppy-disk",
                ],
            ),
            (
                "ri",
                "Remix Icon",
                [
                    "home-line",
                    "settings-3-line",
                    "check-line",
                    "close-line",
                    "search-line",
                    "add-line",
                    "subtract-line",
                    "delete-bin-line",
                    "edit-line",
                    "save-line",
                ],
            ),
            (
                "msc",
                "Microsoft Codicons",
                [
                    "home",
                    "gear",
                    "check",
                    "close",
                    "search",
                    "add",
                    "remove",
                    "trash",
                    "edit",
                    "save",
                ],
            ),
        ]

        for prefix, name, icons in fonts_info:
            group = QGroupBox(f"{name} ({prefix})")
            group_layout = QHBoxLayout(group)
            group_layout.setSpacing(15)

            for icon_name in icons:
                try:
                    icon_widget = QToolButton()
                    icon_widget.setIcon(qta.icon(f"{prefix}.{icon_name}"))
                    icon_widget.setIconSize(QSize(32, 32))
                    icon_widget.setToolTip(f"{prefix}.{icon_name}")
                    icon_widget.setFixedSize(50, 50)
                    group_layout.addWidget(icon_widget)
                except Exception:
                    pass

            group_layout.addStretch()
            layout.addWidget(group)

        layout.addStretch()
        self.setWidget(container)


class ColorShowcasePage(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)

        basic_colors_group = QGroupBox("Basic Colors")
        basic_layout = QHBoxLayout(basic_colors_group)

        colors = [
            "red",
            "green",
            "blue",
            "orange",
            "purple",
            "cyan",
            "magenta",
            "yellow",
            "white",
            "gray",
        ]
        for color in colors:
            btn = QToolButton()
            btn.setIcon(qta.icon("fa6s.star", color=color))
            btn.setIconSize(QSize(40, 40))
            btn.setToolTip(color)
            btn.setFixedSize(60, 60)
            basic_layout.addWidget(btn)

        basic_layout.addStretch()
        layout.addWidget(basic_colors_group)

        hex_colors_group = QGroupBox("Hex Colors")
        hex_layout = QHBoxLayout(hex_colors_group)

        hex_colors = [
            "#FF5733",
            "#33FF57",
            "#3357FF",
            "#FF33F5",
            "#33FFF5",
            "#F5FF33",
            "#FF8C00",
            "#8B00FF",
            "#00FF7F",
            "#DC143C",
        ]
        for hex_color in hex_colors:
            btn = QToolButton()
            btn.setIcon(qta.icon("fa6s.heart", color=hex_color))
            btn.setIconSize(QSize(40, 40))
            btn.setToolTip(hex_color)
            btn.setFixedSize(60, 60)
            hex_layout.addWidget(btn)

        hex_layout.addStretch()
        layout.addWidget(hex_colors_group)

        state_colors_group = QGroupBox(
            "State-Based Colors (Normal / Active / Disabled / Selected)"
        )
        state_layout = QVBoxLayout(state_colors_group)

        info_label = QLabel("Icons can have different colors for different states:")
        state_layout.addWidget(info_label)

        states_row = QHBoxLayout()

        for state_name, kwargs in [
            ("Normal: Blue", {"color": "blue"}),
            ("With Active: Orange", {"color": "blue", "color_active": "orange"}),
            ("With Disabled: Gray", {"color": "blue", "color_disabled": "gray"}),
            (
                "All States",
                {
                    "color": "blue",
                    "color_active": "orange",
                    "color_disabled": "gray",
                    "color_selected": "green",
                },
            ),
        ]:
            frame = QFrame()
            frame.setFrameStyle(QFrame.Box)
            frame_layout = QVBoxLayout(frame)

            btn = QPushButton()
            btn.setIcon(qta.icon("fa6s.bell", **kwargs))
            btn.setIconSize(QSize(32, 32))
            frame_layout.addWidget(btn)

            label = QLabel(state_name)
            label.setAlignment(Qt.AlignCenter)
            label.setWordWrap(True)
            frame_layout.addWidget(label)

            states_row.addWidget(frame)

        states_row.addStretch()
        state_layout.addLayout(states_row)
        layout.addWidget(state_colors_group)

        opacity_group = QGroupBox("Opacity Levels")
        opacity_layout = QHBoxLayout(opacity_group)

        for opacity in [1.0, 0.8, 0.6, 0.4, 0.2]:
            btn = QToolButton()
            btn.setIcon(qta.icon("fa6s.circle", color="blue", opacity=opacity))
            btn.setIconSize(QSize(40, 40))
            btn.setToolTip(f"Opacity: {opacity}")
            btn.setFixedSize(60, 60)
            opacity_layout.addWidget(btn)

        opacity_layout.addStretch()
        layout.addWidget(opacity_group)

        layout.addStretch()
        self.setWidget(container)


class ScaleShowcasePage(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)

        scale_group = QGroupBox("Scale Factor Examples")
        scale_layout = QHBoxLayout(scale_group)

        for scale in [0.5, 0.75, 1.0, 1.25, 1.5]:
            frame = QFrame()
            frame.setFrameStyle(QFrame.Box)
            frame.setFixedSize(80, 100)
            frame_layout = QVBoxLayout(frame)

            btn = QToolButton()
            btn.setIcon(qta.icon("fa6s.rocket", color="#3498db", scale_factor=scale))
            btn.setIconSize(QSize(50, 50))
            btn.setFixedSize(60, 60)
            frame_layout.addWidget(btn, alignment=Qt.AlignCenter)

            label = QLabel(f"{scale}x")
            label.setAlignment(Qt.AlignCenter)
            frame_layout.addWidget(label)

            scale_layout.addWidget(frame)

        scale_layout.addStretch()
        layout.addWidget(scale_group)

        size_group = QGroupBox("Different Icon Sizes (via setIconSize)")
        size_layout = QHBoxLayout(size_group)

        for size in [16, 24, 32, 48, 64, 96]:
            frame = QFrame()
            frame.setFrameStyle(QFrame.Box)
            frame.setMinimumSize(110, 130)
            frame_layout = QVBoxLayout(frame)

            btn = QToolButton()
            btn.setIcon(qta.icon("fa6s.globe", color="#9b59b6"))
            btn.setIconSize(QSize(size, size))
            frame_layout.addWidget(btn, alignment=Qt.AlignCenter)

            label = QLabel(f"{size}x{size}")
            label.setAlignment(Qt.AlignCenter)
            frame_layout.addWidget(label)

            size_layout.addWidget(frame)

        size_layout.addStretch()
        layout.addWidget(size_group)

        layout.addStretch()
        self.setWidget(container)


class TransformShowcasePage(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)

        rotation_group = QGroupBox("Rotation (rotated parameter)")
        rotation_layout = QHBoxLayout(rotation_group)

        for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
            frame = QFrame()
            frame.setFrameStyle(QFrame.Box)
            frame.setFixedSize(70, 90)
            frame_layout = QVBoxLayout(frame)

            btn = QToolButton()
            btn.setIcon(qta.icon("fa6s.arrow-up", color="#e74c3c", rotated=angle))
            btn.setIconSize(QSize(32, 32))
            frame_layout.addWidget(btn, alignment=Qt.AlignCenter)

            label = QLabel(f"{angle}°")
            label.setAlignment(Qt.AlignCenter)
            frame_layout.addWidget(label)

            rotation_layout.addWidget(frame)

        rotation_layout.addStretch()
        layout.addWidget(rotation_group)

        flip_group = QGroupBox("Flip Transformations")
        flip_layout = QHBoxLayout(flip_group)

        flip_options = [
            ("Original", {}),
            ("H-Flip", {"hflip": True}),
            ("V-Flip", {"vflip": True}),
            ("Both", {"hflip": True, "vflip": True}),
        ]

        for name, kwargs in flip_options:
            frame = QFrame()
            frame.setFrameStyle(QFrame.Box)
            frame.setFixedSize(80, 100)
            frame_layout = QVBoxLayout(frame)

            btn = QToolButton()
            btn.setIcon(qta.icon("fa6s.thumbs-up", color="#27ae60", **kwargs))
            btn.setIconSize(QSize(40, 40))
            frame_layout.addWidget(btn, alignment=Qt.AlignCenter)

            label = QLabel(name)
            label.setAlignment(Qt.AlignCenter)
            frame_layout.addWidget(label)

            flip_layout.addWidget(frame)

        flip_layout.addStretch()
        layout.addWidget(flip_group)

        offset_group = QGroupBox("Offset Examples")
        offset_layout = QHBoxLayout(offset_group)

        offsets = [
            ("Center", (0, 0)),
            ("Left", (-0.2, 0)),
            ("Right", (0.2, 0)),
            ("Up", (0, -0.2)),
            ("Down", (0, 0.2)),
        ]

        for name, offset in offsets:
            frame = QFrame()
            frame.setFrameStyle(QFrame.Box)
            frame.setFixedSize(80, 100)
            frame_layout = QVBoxLayout(frame)

            btn = QToolButton()
            btn.setIcon(qta.icon("fa6s.crosshairs", color="#f39c12", offset=offset))
            btn.setIconSize(QSize(40, 40))
            frame_layout.addWidget(btn, alignment=Qt.AlignCenter)

            label = QLabel(name)
            label.setAlignment(Qt.AlignCenter)
            frame_layout.addWidget(label)

            offset_layout.addWidget(frame)

        offset_layout.addStretch()
        layout.addWidget(offset_group)

        layout.addStretch()
        self.setWidget(container)


class AnimationShowcasePage(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.animations = []

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)

        spin_group = QGroupBox("Spin Animation")
        spin_layout = QVBoxLayout(spin_group)

        spin_desc = QLabel(
            "Smooth continuous rotation. Parameters: interval (ms), step (degrees)"
        )
        spin_layout.addWidget(spin_desc)

        spin_row = QHBoxLayout()

        spin_configs = [
            ("Default (10ms, 1°)", 10, 1),
            ("Fast (5ms, 2°)", 5, 2),
            ("Slow (20ms, 1°)", 20, 1),
            ("Choppy (50ms, 5°)", 50, 5),
        ]

        for name, interval, step in spin_configs:
            frame = QFrame()
            frame.setFrameStyle(QFrame.Box)
            frame.setFixedSize(120, 120)
            frame_layout = QVBoxLayout(frame)

            btn = QToolButton()
            spin_anim = Spin(btn, interval=interval, step=step)
            self.animations.append(spin_anim)
            btn.setIcon(qta.icon("fa6s.spinner", color="#3498db", animation=spin_anim))
            btn.setIconSize(QSize(40, 40))
            frame_layout.addWidget(btn, alignment=Qt.AlignCenter)

            label = QLabel(name)
            label.setAlignment(Qt.AlignCenter)
            label.setWordWrap(True)
            frame_layout.addWidget(label)

            spin_row.addWidget(frame)

        spin_row.addStretch()
        spin_layout.addLayout(spin_row)
        layout.addWidget(spin_group)

        pulse_group = QGroupBox("Pulse Animation")
        pulse_layout = QVBoxLayout(pulse_group)

        pulse_desc = QLabel(
            "Stepped rotation (300ms interval, 45° steps) - creates a 'ticking' effect"
        )
        pulse_layout.addWidget(pulse_desc)

        pulse_row = QHBoxLayout()

        pulse_icons = [
            ("fa6s.gear", "Gear"),
            ("fa6s.rotate", "Rotate"),
            ("fa6s.sun", "Sun"),
            ("fa6s.compass", "Compass"),
        ]

        for icon_name, label_text in pulse_icons:
            frame = QFrame()
            frame.setFrameStyle(QFrame.Box)
            frame.setFixedSize(100, 100)
            frame_layout = QVBoxLayout(frame)

            btn = QToolButton()
            pulse_anim = Pulse(btn)
            self.animations.append(pulse_anim)
            btn.setIcon(qta.icon(icon_name, color="#e74c3c", animation=pulse_anim))
            btn.setIconSize(QSize(40, 40))
            frame_layout.addWidget(btn, alignment=Qt.AlignCenter)

            label = QLabel(label_text)
            label.setAlignment(Qt.AlignCenter)
            frame_layout.addWidget(label)

            pulse_row.addWidget(frame)

        pulse_row.addStretch()
        pulse_layout.addLayout(pulse_row)
        layout.addWidget(pulse_group)

        control_group = QGroupBox("Animation Controls")
        control_layout = QVBoxLayout(control_group)

        control_row = QHBoxLayout()

        self.controlled_btn = QToolButton()
        self.controlled_anim = Spin(
            self.controlled_btn, interval=10, step=1, autostart=False
        )
        self.animations.append(self.controlled_anim)
        self.controlled_btn.setIcon(
            qta.icon(
                "fa6s.circle-notch", color="#9b59b6", animation=self.controlled_anim
            )
        )
        self.controlled_btn.setIconSize(QSize(64, 64))
        self.controlled_btn.setFixedSize(80, 80)
        control_row.addWidget(self.controlled_btn)

        btn_layout = QVBoxLayout()

        start_btn = QPushButton("Start Animation")
        start_btn.clicked.connect(self.controlled_anim.start)
        btn_layout.addWidget(start_btn)

        stop_btn = QPushButton("Stop Animation")
        stop_btn.clicked.connect(self.controlled_anim.stop)
        btn_layout.addWidget(stop_btn)

        control_row.addLayout(btn_layout)
        control_row.addStretch()

        control_layout.addLayout(control_row)
        layout.addWidget(control_group)

        layout.addStretch()
        self.setWidget(container)


class StackedIconsPage(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)

        basic_stack_group = QGroupBox("Basic Stacked Icons")
        basic_layout = QHBoxLayout(basic_stack_group)

        stacked_examples = [
            (
                ["fa6s.square", "fa6s.terminal"],
                [{"color": "#34495e"}, {"color": "white", "scale_factor": 0.6}],
                "Terminal",
            ),
            (
                ["fa6s.circle", "fa6s.play"],
                [
                    {"color": "#27ae60"},
                    {"color": "white", "scale_factor": 0.5, "offset": (0.05, 0)},
                ],
                "Play",
            ),
            (
                ["fa6s.certificate", "fa6s.check"],
                [{"color": "#f1c40f"}, {"color": "white", "scale_factor": 0.5}],
                "Verified",
            ),
            (
                ["fa6s.cloud", "fa6s.arrow-down"],
                [
                    {"color": "#3498db"},
                    {"color": "white", "scale_factor": 0.4, "offset": (0, 0.1)},
                ],
                "Download",
            ),
            (
                ["fa6s.folder", "fa6s.plus"],
                [
                    {"color": "#e67e22"},
                    {"color": "white", "scale_factor": 0.4, "offset": (0.1, 0.1)},
                ],
                "New Folder",
            ),
        ]

        for icons, options, label_text in stacked_examples:
            frame = QFrame()
            frame.setFrameStyle(QFrame.Box)
            frame.setFixedSize(100, 100)
            frame_layout = QVBoxLayout(frame)

            btn = QToolButton()
            btn.setIcon(qta.icon(*icons, options=options))
            btn.setIconSize(QSize(48, 48))
            frame_layout.addWidget(btn, alignment=Qt.AlignCenter)

            label = QLabel(label_text)
            label.setAlignment(Qt.AlignCenter)
            frame_layout.addWidget(label)

            basic_layout.addWidget(frame)

        basic_layout.addStretch()
        layout.addWidget(basic_stack_group)

        badge_group = QGroupBox("Badge/Overlay Patterns")
        badge_layout = QHBoxLayout(badge_group)

        badge_examples = [
            (
                ["fa6s.envelope", "fa6s.circle"],
                [
                    {"color": "#7f8c8d"},
                    {"color": "#e74c3c", "scale_factor": 0.4, "offset": (0.25, -0.25)},
                ],
                "Notification",
            ),
            (
                ["fa6s.bell", "fa6s.exclamation"],
                [
                    {"color": "#3498db"},
                    {"color": "#e74c3c", "scale_factor": 0.5, "offset": (0.2, -0.2)},
                ],
                "Alert",
            ),
            (
                ["fa6s.user", "fa6s.check"],
                [
                    {"color": "#9b59b6"},
                    {"color": "#27ae60", "scale_factor": 0.4, "offset": (0.25, 0.2)},
                ],
                "Verified User",
            ),
            (
                ["fa6s.file", "fa6s.lock"],
                [
                    {"color": "#34495e"},
                    {"color": "#e74c3c", "scale_factor": 0.4, "offset": (0.2, 0.15)},
                ],
                "Locked File",
            ),
        ]

        for icons, options, label_text in badge_examples:
            frame = QFrame()
            frame.setFrameStyle(QFrame.Box)
            frame.setFixedSize(100, 100)
            frame_layout = QVBoxLayout(frame)

            btn = QToolButton()
            btn.setIcon(qta.icon(*icons, options=options))
            btn.setIconSize(QSize(48, 48))
            frame_layout.addWidget(btn, alignment=Qt.AlignCenter)

            label = QLabel(label_text)
            label.setAlignment(Qt.AlignCenter)
            frame_layout.addWidget(label)

            badge_layout.addWidget(frame)

        badge_layout.addStretch()
        layout.addWidget(badge_group)

        ban_group = QGroupBox("Ban/Prohibition Pattern")
        ban_layout = QHBoxLayout(ban_group)

        ban_examples = [
            ("fa6s.camera", "No Camera"),
            ("fa6s.microphone", "Muted"),
            ("fa6s.volume-high", "No Sound"),
            ("fa6s.wifi", "No WiFi"),
            ("fa6s.mobile", "No Phone"),
        ]

        for base_icon, label_text in ban_examples:
            frame = QFrame()
            frame.setFrameStyle(QFrame.Box)
            frame.setFixedSize(100, 100)
            frame_layout = QVBoxLayout(frame)

            btn = QToolButton()
            btn.setIcon(
                qta.icon(
                    base_icon,
                    "fa6s.ban",
                    options=[
                        {"color": "#7f8c8d", "scale_factor": 0.6},
                        {"color": "#e74c3c", "opacity": 0.8},
                    ],
                )
            )
            btn.setIconSize(QSize(48, 48))
            frame_layout.addWidget(btn, alignment=Qt.AlignCenter)

            label = QLabel(label_text)
            label.setAlignment(Qt.AlignCenter)
            frame_layout.addWidget(label)

            ban_layout.addWidget(frame)

        ban_layout.addStretch()
        layout.addWidget(ban_group)

        layout.addStretch()
        self.setWidget(container)


class IconWidgetPage(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)

        basic_group = QGroupBox("Basic IconWidget Usage")
        basic_layout = QHBoxLayout(basic_group)

        sizes = [16, 24, 32, 48, 64]
        for size in sizes:
            frame = QFrame()
            frame.setFrameStyle(QFrame.Box)
            frame.setMinimumSize(90, 100)
            frame_layout = QVBoxLayout(frame)

            icon_widget = qta.IconWidget(
                "fa6s.star", color="#f1c40f", size=QSize(size, size)
            )
            frame_layout.addWidget(icon_widget, alignment=Qt.AlignCenter)

            label = QLabel(f"{size}px")
            label.setAlignment(Qt.AlignCenter)
            frame_layout.addWidget(label)

            basic_layout.addWidget(frame)

        basic_layout.addStretch()
        layout.addWidget(basic_group)

        styled_group = QGroupBox("Styled IconWidgets")
        styled_layout = QHBoxLayout(styled_group)

        styles = [
            ("fa6s.heart", "#e74c3c"),
            ("fa6s.thumbs-up", "#3498db"),
            ("fa6s.circle-check", "#27ae60"),
            ("fa6s.triangle-exclamation", "#f39c12"),
            ("fa6s.circle-info", "#9b59b6"),
        ]

        for icon_name, color in styles:
            icon_widget = qta.IconWidget(icon_name, color=color, size=QSize(48, 48))
            styled_layout.addWidget(icon_widget)

        styled_layout.addStretch()
        layout.addWidget(styled_group)

        layout.addStretch()
        self.setWidget(container)


class ThemePage(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)

        theme_group = QGroupBox("Theme Switching")
        theme_layout = QVBoxLayout(theme_group)

        desc = QLabel(
            "QtAwesome provides built-in dark and light themes that affect the entire application palette."
        )
        desc.setWordWrap(True)
        theme_layout.addWidget(desc)

        btn_row = QHBoxLayout()

        dark_btn = QPushButton("Apply Dark Theme")
        dark_btn.setIcon(qta.icon("fa6s.moon", color="#f1c40f"))
        dark_btn.clicked.connect(lambda: qta.dark(QApplication.instance()))
        btn_row.addWidget(dark_btn)

        light_btn = QPushButton("Apply Light Theme")
        light_btn.setIcon(qta.icon("fa6s.sun", color="#f39c12"))
        light_btn.clicked.connect(lambda: qta.light(QApplication.instance()))
        btn_row.addWidget(light_btn)

        btn_row.addStretch()
        theme_layout.addLayout(btn_row)
        layout.addWidget(theme_group)

        preview_group = QGroupBox("Icon Preview (Colors adapt to theme)")
        preview_layout = QGridLayout(preview_group)

        preview_icons = [
            "fa6s.house",
            "fa6s.gear",
            "fa6s.user",
            "fa6s.envelope",
            "fa6s.bell",
            "fa6s.calendar",
            "fa6s.folder",
            "fa6s.file",
        ]

        for i, icon_name in enumerate(preview_icons):
            btn = QToolButton()
            btn.setIcon(qta.icon(icon_name))
            btn.setIconSize(QSize(32, 32))
            btn.setToolTip(icon_name)
            preview_layout.addWidget(btn, i // 4, i % 4)

        layout.addWidget(preview_group)

        defaults_group = QGroupBox("Setting Global Defaults")
        defaults_layout = QVBoxLayout(defaults_group)

        defaults_desc = QLabel(
            "You can set default options for all icons using qta.set_defaults().\n"
            "Valid options: color, color_disabled, opacity, scale_factor, etc."
        )
        defaults_desc.setWordWrap(True)
        defaults_layout.addWidget(defaults_desc)

        layout.addWidget(defaults_group)

        layout.addStretch()
        self.setWidget(container)


class RealWorldPage(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.animations = []

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)

        toolbar_group = QGroupBox("Toolbar Example")
        toolbar_layout = QHBoxLayout(toolbar_group)

        toolbar_items = [
            ("fa6s.file", "New"),
            ("fa6s.folder-open", "Open"),
            ("fa6s.floppy-disk", "Save"),
            ("fa6s.print", "Print"),
            ("fa6s.scissors", "Cut"),
            ("fa6s.copy", "Copy"),
            ("fa6s.paste", "Paste"),
            ("fa6s.rotate-left", "Undo"),
            ("fa6s.rotate-right", "Redo"),
        ]

        for icon_name, tooltip in toolbar_items:
            btn = QToolButton()
            btn.setIcon(qta.icon(icon_name, color="#2c3e50"))
            btn.setIconSize(QSize(24, 24))
            btn.setToolTip(tooltip)
            toolbar_layout.addWidget(btn)

        toolbar_layout.addStretch()
        layout.addWidget(toolbar_group)

        nav_group = QGroupBox("Navigation Menu Example")
        nav_layout = QVBoxLayout(nav_group)

        nav_items = [
            ("fa6s.house", "Home"),
            ("fa6s.chart-line", "Dashboard"),
            ("fa6s.users", "Users"),
            ("fa6s.envelope", "Messages"),
            ("fa6s.gear", "Settings"),
        ]

        for icon_name, text in nav_items:
            btn = QPushButton(f"  {text}")
            btn.setIcon(qta.icon(icon_name, color="#3498db"))
            btn.setIconSize(QSize(20, 20))
            btn.setStyleSheet("text-align: left; padding: 8px;")
            nav_layout.addWidget(btn)

        layout.addWidget(nav_group)

        status_group = QGroupBox("Status Indicators")
        status_layout = QHBoxLayout(status_group)

        statuses = [
            ("fa6s.circle-check", "#27ae60", "Online"),
            ("fa6s.circle-xmark", "#e74c3c", "Offline"),
            ("fa6s.clock", "#f39c12", "Pending"),
            ("fa6s.circle-exclamation", "#e67e22", "Warning"),
            ("fa6s.spinner", "#3498db", "Loading"),
        ]

        for i, (icon_name, color, text) in enumerate(statuses):
            frame = QFrame()
            frame_layout = QHBoxLayout(frame)
            frame_layout.setContentsMargins(5, 5, 5, 5)

            if text == "Loading":
                spin = Spin(frame, interval=10, step=2)
                self.animations.append(spin)
                icon = qta.icon(icon_name, color=color, animation=spin)
            else:
                icon = qta.icon(icon_name, color=color)

            icon_label = QLabel()
            icon_label.setPixmap(icon.pixmap(QSize(16, 16)))
            frame_layout.addWidget(icon_label)

            text_label = QLabel(text)
            frame_layout.addWidget(text_label)

            status_layout.addWidget(frame)

        status_layout.addStretch()
        layout.addWidget(status_group)

        form_group = QGroupBox("Form Input Example")
        form_layout = QGridLayout(form_group)

        user_input = QLineEdit()
        user_input.setPlaceholderText("Username")
        user_btn = QToolButton()
        user_btn.setIcon(qta.icon("fa6s.user", color="#7f8c8d"))
        form_layout.addWidget(user_btn, 0, 0)
        form_layout.addWidget(user_input, 0, 1)

        email_input = QLineEdit()
        email_input.setPlaceholderText("Email")
        email_btn = QToolButton()
        email_btn.setIcon(qta.icon("fa6s.envelope", color="#7f8c8d"))
        form_layout.addWidget(email_btn, 1, 0)
        form_layout.addWidget(email_input, 1, 1)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Search...")
        search_btn = QToolButton()
        search_btn.setIcon(qta.icon("fa6s.magnifying-glass", color="#7f8c8d"))
        form_layout.addWidget(search_btn, 2, 0)
        form_layout.addWidget(search_input, 2, 1)

        layout.addWidget(form_group)

        layout.addStretch()
        self.setWidget(container)


class IconListWidget(QListWidget):
    icon_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setViewMode(QListWidget.IconMode)
        self.setIconSize(QSize(32, 32))
        self.setSpacing(5)
        self.setResizeMode(QListWidget.Adjust)
        self.setWordWrap(True)
        self.setUniformItemSizes(True)
        self.itemClicked.connect(self._on_item_clicked)

    def _on_item_clicked(self, item):
        self.icon_selected.emit(item.data(Qt.UserRole))


class ExportDialog(QWidget):
    def __init__(self, icon_name, size, parent=None):
        super().__init__(parent, Qt.Window)
        self.setWindowTitle("Export Icon")
        self.setMinimumWidth(400)
        self.icon_name = icon_name
        self.export_size = size
        self.setWindowModality(Qt.ApplicationModal)
        self._setup_ui()
        self._update_preview()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout(preview_group)

        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumSize(150, 150)
        preview_layout.addWidget(self.preview_label)

        self.icon_name_label = QLabel(self.icon_name)
        self.icon_name_label.setAlignment(Qt.AlignCenter)
        self.icon_name_label.setStyleSheet("font-weight: bold;")
        preview_layout.addWidget(self.icon_name_label)

        self.size_label = QLabel(
            f"Export size: {self.export_size} x {self.export_size} px"
        )
        self.size_label.setAlignment(Qt.AlignCenter)
        self.size_label.setStyleSheet("color: #7f8c8d;")
        preview_layout.addWidget(self.size_label)

        layout.addWidget(preview_group)

        color_group = QGroupBox("Color")
        color_layout = QHBoxLayout(color_group)

        self.color_input = QLineEdit("#3498db")
        self.color_input.textChanged.connect(self._update_preview)
        color_layout.addWidget(self.color_input)

        color_btn = QPushButton("Pick...")
        color_btn.clicked.connect(self._pick_color)
        color_layout.addWidget(color_btn)

        layout.addWidget(color_group)

        scale_opacity_group = QGroupBox("Scale && Opacity")
        scale_opacity_layout = QGridLayout(scale_opacity_group)

        scale_opacity_layout.addWidget(QLabel("Scale Factor:"), 0, 0)
        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setRange(0.1, 3.0)
        self.scale_spin.setValue(1.0)
        self.scale_spin.setSingleStep(0.1)
        self.scale_spin.valueChanged.connect(self._update_preview)
        scale_opacity_layout.addWidget(self.scale_spin, 0, 1)

        scale_opacity_layout.addWidget(QLabel("Opacity:"), 1, 0)
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self._update_preview)
        scale_opacity_layout.addWidget(self.opacity_slider, 1, 1)

        self.opacity_label = QLabel("100%")
        self.opacity_label.setMinimumWidth(45)
        scale_opacity_layout.addWidget(self.opacity_label, 1, 2)

        layout.addWidget(scale_opacity_group)

        rotation_group = QGroupBox("Rotation")
        rotation_layout = QHBoxLayout(rotation_group)

        self.rotation_slider = QSlider(Qt.Horizontal)
        self.rotation_slider.setRange(0, 359)
        self.rotation_slider.setValue(0)
        self.rotation_slider.valueChanged.connect(self._update_preview)
        rotation_layout.addWidget(self.rotation_slider)

        self.rotation_label = QLabel("0°")
        self.rotation_label.setMinimumWidth(40)
        rotation_layout.addWidget(self.rotation_label)

        layout.addWidget(rotation_group)

        flip_group = QGroupBox("Flip")
        flip_layout = QHBoxLayout(flip_group)

        self.hflip_check = QCheckBox("Horizontal")
        self.hflip_check.stateChanged.connect(self._update_preview)
        flip_layout.addWidget(self.hflip_check)

        self.vflip_check = QCheckBox("Vertical")
        self.vflip_check.stateChanged.connect(self._update_preview)
        flip_layout.addWidget(self.vflip_check)

        flip_layout.addStretch()
        layout.addWidget(flip_group)

        offset_group = QGroupBox("Offset")
        offset_layout = QHBoxLayout(offset_group)

        offset_layout.addWidget(QLabel("X:"))
        self.offset_x_spin = QDoubleSpinBox()
        self.offset_x_spin.setRange(-0.5, 0.5)
        self.offset_x_spin.setValue(0.0)
        self.offset_x_spin.setSingleStep(0.05)
        self.offset_x_spin.valueChanged.connect(self._update_preview)
        offset_layout.addWidget(self.offset_x_spin)

        offset_layout.addWidget(QLabel("Y:"))
        self.offset_y_spin = QDoubleSpinBox()
        self.offset_y_spin.setRange(-0.5, 0.5)
        self.offset_y_spin.setValue(0.0)
        self.offset_y_spin.setSingleStep(0.05)
        self.offset_y_spin.valueChanged.connect(self._update_preview)
        offset_layout.addWidget(self.offset_y_spin)

        offset_layout.addStretch()
        layout.addWidget(offset_group)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)
        btn_layout.addWidget(cancel_btn)

        export_btn = QPushButton("Export")
        export_btn.setDefault(True)
        export_btn.clicked.connect(self._do_export)
        btn_layout.addWidget(export_btn)

        layout.addLayout(btn_layout)

    def _pick_color(self):
        color = QColorDialog.getColor(QColor(self.color_input.text()), self)
        if color.isValid():
            self.color_input.setText(color.name())

    def _get_icon_kwargs(self):
        kwargs = {
            "color": self.color_input.text(),
            "scale_factor": self.scale_spin.value(),
            "opacity": self.opacity_slider.value() / 100.0,
        }

        rotation = self.rotation_slider.value()
        if rotation != 0:
            kwargs["rotated"] = rotation

        if self.hflip_check.isChecked():
            kwargs["hflip"] = True

        if self.vflip_check.isChecked():
            kwargs["vflip"] = True

        offset_x = self.offset_x_spin.value()
        offset_y = self.offset_y_spin.value()
        if offset_x != 0 or offset_y != 0:
            kwargs["offset"] = (offset_x, offset_y)

        return kwargs

    def _update_preview(self):
        self.opacity_label.setText(f"{self.opacity_slider.value()}%")
        self.rotation_label.setText(f"{self.rotation_slider.value()}°")

        kwargs = self._get_icon_kwargs()

        try:
            icon = qta.icon(self.icon_name, **kwargs)
            pixmap = icon.pixmap(QSize(128, 128))
            self.preview_label.setPixmap(pixmap)
        except Exception:
            pass

    def _do_export(self):
        kwargs = self._get_icon_kwargs()

        try:
            icon = qta.icon(self.icon_name, **kwargs)
        except Exception:
            return

        default_filename = (
            self.icon_name.replace(".", "_")
            + f"_{self.export_size}x{self.export_size}.png"
        )

        filepath, _ = QFileDialog.getSaveFileName(
            self, "Export Icon as PNG", default_filename, "PNG Files (*.png)"
        )

        if filepath:
            if not filepath.lower().endswith(".png"):
                filepath += ".png"
            pixmap = icon.pixmap(QSize(self.export_size, self.export_size))
            pixmap.save(filepath, "PNG")
            self.close()


class PlaygroundPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_animation = None
        self.all_icons = []
        self._load_all_icons()
        self._setup_ui()

    def _load_all_icons(self):
        qta._instance()
        charmap = qta._resource["iconic"].charmap
        for prefix, icons in charmap.items():
            for icon_name in icons.keys():
                self.all_icons.append(f"{prefix}.{icon_name}")
        self.all_icons.sort()

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        splitter = QSplitter(Qt.Horizontal)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        search_group = QGroupBox("Search Icons")
        search_layout = QVBoxLayout(search_group)

        filter_row = QHBoxLayout()

        self.font_filter = QComboBox()
        self.font_filter.addItem("All Fonts", "")
        qta._instance()
        charmap = qta._resource["iconic"].charmap
        font_info = {
            "fa5": "Font Awesome 5 Regular",
            "fa5s": "Font Awesome 5 Solid",
            "fa5b": "Font Awesome 5 Brands",
            "fa6": "Font Awesome 6 Regular",
            "fa6s": "Font Awesome 6 Solid",
            "fa6b": "Font Awesome 6 Brands",
            "ei": "Elusive Icons",
            "mdi": "Material Design Icons 5",
            "mdi6": "Material Design Icons 6",
            "ph": "Phosphor Icons",
            "ri": "Remix Icon",
            "msc": "Microsoft Codicons",
        }
        for prefix in sorted(charmap.keys()):
            display_name = font_info.get(prefix, prefix)
            count = len(charmap[prefix])
            self.font_filter.addItem(f"{display_name} ({count})", prefix)
        self.font_filter.currentIndexChanged.connect(self._filter_icons_immediate)
        filter_row.addWidget(self.font_filter)

        search_layout.addLayout(filter_row)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type to search icons...")
        self.search_input.setClearButtonEnabled(True)

        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.setInterval(700)
        self.search_timer.timeout.connect(self._filter_icons)
        self.search_input.textChanged.connect(self._on_search_changed)

        search_layout.addWidget(self.search_input)

        self.result_count = QLabel(f"Showing {len(self.all_icons)} icons")
        search_layout.addWidget(self.result_count)

        left_layout.addWidget(search_group)

        self.icon_list = IconListWidget()
        self.icon_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.icon_list.customContextMenuRequested.connect(self._show_icon_context_menu)
        self.icon_list.icon_selected.connect(self._on_icon_selected)
        left_layout.addWidget(self.icon_list)

        self._populate_icon_list(self.all_icons)

        right_panel = QScrollArea()
        right_panel.setWidgetResizable(True)
        right_panel.setMinimumWidth(350)

        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setSpacing(15)

        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout(preview_group)

        self.preview_button = QToolButton()
        self.preview_button.setIconSize(QSize(128, 128))
        self.preview_button.setFixedSize(150, 150)
        self.preview_button.setIcon(qta.icon("fa6s.icons", color="#3498db"))
        preview_layout.addWidget(self.preview_button, alignment=Qt.AlignCenter)

        self.selected_icon_label = QLabel("No icon selected")
        self.selected_icon_label.setAlignment(Qt.AlignCenter)
        self.selected_icon_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        preview_layout.addWidget(self.selected_icon_label)

        self.code_label = QLabel("")
        self.code_label.setAlignment(Qt.AlignCenter)
        self.code_label.setWordWrap(True)
        self.code_label.setStyleSheet(
            "font-family: monospace; font-size: 10px; color: #7f8c8d;"
        )
        preview_layout.addWidget(self.code_label)

        copy_btn = QPushButton("Copy Code")
        copy_btn.clicked.connect(self._copy_code)
        preview_layout.addWidget(copy_btn)

        right_layout.addWidget(preview_group)

        color_group = QGroupBox("Color")
        color_layout = QHBoxLayout(color_group)

        self.color_input = QLineEdit("#3498db")
        self.color_input.setMaximumWidth(100)
        self.color_input.textChanged.connect(self._update_preview)
        color_layout.addWidget(self.color_input)

        color_btn = QPushButton("Pick...")
        color_btn.clicked.connect(self._pick_color)
        color_layout.addWidget(color_btn)

        color_layout.addStretch()
        right_layout.addWidget(color_group)

        size_group = QGroupBox("Size")
        size_layout = QHBoxLayout(size_group)

        size_layout.addWidget(QLabel("Icon Size:"))
        self.size_spin = QSpinBox()
        self.size_spin.setRange(16, 256)
        self.size_spin.setValue(128)
        self.size_spin.valueChanged.connect(self._update_preview)
        size_layout.addWidget(self.size_spin)

        size_layout.addWidget(QLabel("Scale Factor:"))
        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setRange(0.1, 3.0)
        self.scale_spin.setValue(1.0)
        self.scale_spin.setSingleStep(0.1)
        self.scale_spin.valueChanged.connect(self._update_preview)
        size_layout.addWidget(self.scale_spin)

        size_layout.addStretch()
        right_layout.addWidget(size_group)

        opacity_group = QGroupBox("Opacity")
        opacity_layout = QHBoxLayout(opacity_group)

        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self._update_preview)
        opacity_layout.addWidget(self.opacity_slider)

        self.opacity_label = QLabel("100%")
        self.opacity_label.setMinimumWidth(40)
        opacity_layout.addWidget(self.opacity_label)

        right_layout.addWidget(opacity_group)

        rotation_group = QGroupBox("Rotation")
        rotation_layout = QHBoxLayout(rotation_group)

        self.rotation_slider = QSlider(Qt.Horizontal)
        self.rotation_slider.setRange(0, 359)
        self.rotation_slider.setValue(0)
        self.rotation_slider.valueChanged.connect(self._update_preview)
        rotation_layout.addWidget(self.rotation_slider)

        self.rotation_label = QLabel("0°")
        self.rotation_label.setMinimumWidth(40)
        rotation_layout.addWidget(self.rotation_label)

        right_layout.addWidget(rotation_group)

        flip_group = QGroupBox("Flip")
        flip_layout = QHBoxLayout(flip_group)

        self.hflip_check = QCheckBox("Horizontal")
        self.hflip_check.stateChanged.connect(self._update_preview)
        flip_layout.addWidget(self.hflip_check)

        self.vflip_check = QCheckBox("Vertical")
        self.vflip_check.stateChanged.connect(self._update_preview)
        flip_layout.addWidget(self.vflip_check)

        flip_layout.addStretch()
        right_layout.addWidget(flip_group)

        offset_group = QGroupBox("Offset")
        offset_layout = QGridLayout(offset_group)

        offset_layout.addWidget(QLabel("X:"), 0, 0)
        self.offset_x_spin = QDoubleSpinBox()
        self.offset_x_spin.setRange(-0.5, 0.5)
        self.offset_x_spin.setValue(0.0)
        self.offset_x_spin.setSingleStep(0.05)
        self.offset_x_spin.valueChanged.connect(self._update_preview)
        offset_layout.addWidget(self.offset_x_spin, 0, 1)

        offset_layout.addWidget(QLabel("Y:"), 0, 2)
        self.offset_y_spin = QDoubleSpinBox()
        self.offset_y_spin.setRange(-0.5, 0.5)
        self.offset_y_spin.setValue(0.0)
        self.offset_y_spin.setSingleStep(0.05)
        self.offset_y_spin.valueChanged.connect(self._update_preview)
        offset_layout.addWidget(self.offset_y_spin, 0, 3)

        right_layout.addWidget(offset_group)

        anim_group = QGroupBox("Animation")
        anim_layout = QVBoxLayout(anim_group)

        anim_type_row = QHBoxLayout()
        anim_type_row.addWidget(QLabel("Type:"))
        self.anim_combo = QComboBox()
        self.anim_combo.addItems(["None", "Spin", "Pulse"])
        self.anim_combo.currentIndexChanged.connect(self._update_preview)
        anim_type_row.addWidget(self.anim_combo)
        anim_type_row.addStretch()
        anim_layout.addLayout(anim_type_row)

        spin_params_row = QHBoxLayout()
        spin_params_row.addWidget(QLabel("Interval (ms):"))
        self.spin_interval = QSpinBox()
        self.spin_interval.setRange(1, 500)
        self.spin_interval.setValue(10)
        self.spin_interval.valueChanged.connect(self._update_preview)
        spin_params_row.addWidget(self.spin_interval)

        spin_params_row.addWidget(QLabel("Step (°):"))
        self.spin_step = QSpinBox()
        self.spin_step.setRange(1, 90)
        self.spin_step.setValue(1)
        self.spin_step.valueChanged.connect(self._update_preview)
        spin_params_row.addWidget(self.spin_step)
        spin_params_row.addStretch()
        anim_layout.addLayout(spin_params_row)

        anim_btn_row = QHBoxLayout()
        self.start_anim_btn = QPushButton("Start")
        self.start_anim_btn.clicked.connect(self._start_animation)
        anim_btn_row.addWidget(self.start_anim_btn)

        self.stop_anim_btn = QPushButton("Stop")
        self.stop_anim_btn.clicked.connect(self._stop_animation)
        anim_btn_row.addWidget(self.stop_anim_btn)
        anim_btn_row.addStretch()
        anim_layout.addLayout(anim_btn_row)

        right_layout.addWidget(anim_group)

        reset_btn = QPushButton("Reset All")
        reset_btn.clicked.connect(self._reset_all)
        right_layout.addWidget(reset_btn)

        right_layout.addStretch()

        right_panel.setWidget(right_container)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([500, 350])

        main_layout.addWidget(splitter)

        self.selected_icon = "fa6s.icons"

    def _populate_icon_list(self, icons):
        self.icon_list.clear()
        for icon_name in icons:
            try:
                item = QListWidgetItem()
                item.setIcon(qta.icon(icon_name))
                item.setText(icon_name.split(".")[-1])
                item.setToolTip(icon_name)
                item.setData(Qt.UserRole, icon_name)
                item.setSizeHint(QSize(80, 60))
                self.icon_list.addItem(item)
            except Exception:
                pass
        self.result_count.setText(f"Showing {self.icon_list.count()} icons")

    def _on_search_changed(self):
        self.search_timer.stop()
        self.search_timer.start()

    def _filter_icons(self):
        search_text = self.search_input.text().lower().strip()
        prefix_filter = self.font_filter.currentData()

        if not search_text:
            filtered = []
            for icon_name in self.all_icons:
                if prefix_filter and not icon_name.startswith(prefix_filter + "."):
                    continue
                filtered.append(icon_name)
            self._populate_icon_list(filtered)
            return

        exact_matches = []
        fuzzy_matches = []

        for icon_name in self.all_icons:
            if prefix_filter and not icon_name.startswith(prefix_filter + "."):
                continue

            icon_lower = icon_name.lower()
            short_name = icon_name.split(".")[-1].lower()

            if search_text in icon_lower:
                if short_name == search_text:
                    exact_matches.insert(0, (icon_name, 100))
                elif short_name.startswith(search_text):
                    exact_matches.append((icon_name, 95))
                else:
                    exact_matches.append((icon_name, 90))
            else:
                score = max(
                    fuzz.ratio(search_text, short_name),
                    fuzz.partial_ratio(search_text, short_name),
                )
                if score >= 60:
                    fuzzy_matches.append((icon_name, score))

        exact_matches.sort(key=lambda x: (-x[1], x[0]))
        fuzzy_matches.sort(key=lambda x: (-x[1], x[0]))

        combined = [item[0] for item in exact_matches] + [
            item[0] for item in fuzzy_matches
        ]

        self._populate_icon_list(combined)

    def _filter_icons_immediate(self):
        self.search_timer.stop()
        self._filter_icons()

    def _on_icon_selected(self, icon_name):
        self.selected_icon = icon_name
        self.selected_icon_label.setText(icon_name)
        self._update_preview()

    def _get_icon_kwargs(self):
        kwargs = {
            "color": self.color_input.text(),
            "scale_factor": self.scale_spin.value(),
            "opacity": self.opacity_slider.value() / 100.0,
        }

        rotation = self.rotation_slider.value()
        if rotation != 0:
            kwargs["rotated"] = rotation

        if self.hflip_check.isChecked():
            kwargs["hflip"] = True

        if self.vflip_check.isChecked():
            kwargs["vflip"] = True

        offset_x = self.offset_x_spin.value()
        offset_y = self.offset_y_spin.value()
        if offset_x != 0 or offset_y != 0:
            kwargs["offset"] = (offset_x, offset_y)

        return kwargs

    def _update_preview(self):
        self.opacity_label.setText(f"{self.opacity_slider.value()}%")
        self.rotation_label.setText(f"{self.rotation_slider.value()}°")

        if self.current_animation:
            self.current_animation.stop()
            self.current_animation = None

        kwargs = self._get_icon_kwargs()

        anim_type = self.anim_combo.currentText()
        if anim_type == "Spin":
            self.current_animation = Spin(
                self.preview_button,
                interval=self.spin_interval.value(),
                step=self.spin_step.value(),
                autostart=True,
            )
            kwargs["animation"] = self.current_animation
        elif anim_type == "Pulse":
            self.current_animation = Pulse(self.preview_button, autostart=True)
            kwargs["animation"] = self.current_animation

        try:
            icon = qta.icon(self.selected_icon, **kwargs)
            size = self.size_spin.value()
            self.preview_button.setIconSize(QSize(size, size))
            self.preview_button.setIcon(icon)

            self._update_code_label(kwargs)
        except Exception as e:
            self.code_label.setText(f"Error: {str(e)}")

    def _update_code_label(self, kwargs):
        code_parts = [f'qta.icon("{self.selected_icon}"']

        for key, value in kwargs.items():
            if key == "animation":
                anim_type = self.anim_combo.currentText()
                if anim_type == "Spin":
                    code_parts.append(
                        f"animation=Spin(widget, interval={self.spin_interval.value()}, step={self.spin_step.value()})"
                    )
                elif anim_type == "Pulse":
                    code_parts.append("animation=Pulse(widget)")
            elif key == "color":
                code_parts.append(f'color="{value}"')
            elif key == "offset":
                code_parts.append(f"offset={value}")
            elif key in ("hflip", "vflip"):
                code_parts.append(f"{key}=True")
            elif key == "opacity" and value != 1.0:
                code_parts.append(f"opacity={value:.2f}")
            elif key == "scale_factor" and value != 1.0:
                code_parts.append(f"scale_factor={value:.2f}")
            elif key == "rotated":
                code_parts.append(f"rotated={value}")

        if len(code_parts) == 1:
            self.code_label.setText(code_parts[0] + ")")
        else:
            self.code_label.setText(
                code_parts[0] + ",\n    " + ",\n    ".join(code_parts[1:]) + ")"
            )

    def _pick_color(self):
        color = QColorDialog.getColor(QColor(self.color_input.text()), self)
        if color.isValid():
            self.color_input.setText(color.name())

    def _start_animation(self):
        if self.current_animation:
            self.current_animation.start()

    def _stop_animation(self):
        if self.current_animation:
            self.current_animation.stop()

    def _reset_all(self):
        self.color_input.setText("#3498db")
        self.size_spin.setValue(128)
        self.scale_spin.setValue(1.0)
        self.opacity_slider.setValue(100)
        self.rotation_slider.setValue(0)
        self.hflip_check.setChecked(False)
        self.vflip_check.setChecked(False)
        self.offset_x_spin.setValue(0.0)
        self.offset_y_spin.setValue(0.0)
        self.anim_combo.setCurrentIndex(0)
        self.spin_interval.setValue(10)
        self.spin_step.setValue(1)
        self._update_preview()

    def _show_icon_context_menu(self, position):
        item = self.icon_list.itemAt(position)
        if not item:
            return

        icon_name = item.data(Qt.UserRole)

        menu = QMenu(self)

        export_menu = menu.addMenu("Export as PNG")

        export_menu.addAction("Note: Exported as PNG (lossless)").setEnabled(False)
        export_menu.addSeparator()

        for size in [128, 256, 512, 1024]:
            action = export_menu.addAction(f"{size} x {size}")
            action.triggered.connect(
                lambda checked, n=icon_name, s=size: self._export_icon(n, s)
            )

        export_menu.addSeparator()
        custom_action = export_menu.addAction("Custom size...")
        custom_action.triggered.connect(lambda: self._export_icon_custom(icon_name))

        menu.exec(self.icon_list.mapToGlobal(position))

    def _export_icon(self, icon_name, size):
        dialog = ExportDialog(icon_name, size, self)
        dialog.show()

    def _export_icon_custom(self, icon_name):
        size, ok = QInputDialog.getInt(
            self,
            "Custom Size",
            "Enter size in pixels (will be square):",
            value=256,
            min=16,
            max=4096,
        )

        if ok:
            self._export_icon(icon_name, size)

    def _copy_code(self):
        clipboard = QApplication.instance().clipboard()
        clipboard.setText(self.code_label.text())


class StackLayerWidget(QFrame):
    layer_changed = Signal()
    delete_requested = Signal(object)
    move_up_requested = Signal(object)
    move_down_requested = Signal(object)

    def __init__(self, icon_name, parent=None):
        super().__init__(parent)
        self.icon_name = icon_name
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet(
            "StackLayerWidget { background-color: #3d3d3d; border-radius: 4px; }"
        )
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        header_row = QHBoxLayout()

        self.icon_preview = QLabel()
        self.icon_preview.setFixedSize(32, 32)
        header_row.addWidget(self.icon_preview)

        self.name_label = QLabel(self.icon_name)
        self.name_label.setStyleSheet("font-weight: bold; font-size: 11px;")
        header_row.addWidget(self.name_label, 1)

        up_btn = QToolButton()
        up_btn.setIcon(qta.icon("fa6s.arrow-up", color="#aaa"))
        up_btn.setFixedSize(24, 24)
        up_btn.setToolTip("Move layer up")
        up_btn.clicked.connect(lambda: self.move_up_requested.emit(self))
        header_row.addWidget(up_btn)

        down_btn = QToolButton()
        down_btn.setIcon(qta.icon("fa6s.arrow-down", color="#aaa"))
        down_btn.setFixedSize(24, 24)
        down_btn.setToolTip("Move layer down")
        down_btn.clicked.connect(lambda: self.move_down_requested.emit(self))
        header_row.addWidget(down_btn)

        delete_btn = QToolButton()
        delete_btn.setIcon(qta.icon("fa6s.xmark", color="#e74c3c"))
        delete_btn.setFixedSize(24, 24)
        delete_btn.setToolTip("Remove layer")
        delete_btn.clicked.connect(lambda: self.delete_requested.emit(self))
        header_row.addWidget(delete_btn)

        layout.addLayout(header_row)

        controls_widget = QWidget()
        controls_layout = QGridLayout(controls_widget)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(4)

        controls_layout.addWidget(QLabel("Color:"), 0, 0)
        self.color_input = QLineEdit("#3498db")
        self.color_input.setMaximumWidth(80)
        self.color_input.textChanged.connect(self._on_changed)
        controls_layout.addWidget(self.color_input, 0, 1)

        color_btn = QToolButton()
        color_btn.setIcon(qta.icon("fa6s.eye-dropper", color="#aaa"))
        color_btn.setFixedSize(24, 24)
        color_btn.clicked.connect(self._pick_color)
        controls_layout.addWidget(color_btn, 0, 2)

        controls_layout.addWidget(QLabel("Scale:"), 0, 3)
        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setRange(0.1, 2.0)
        self.scale_spin.setValue(1.0)
        self.scale_spin.setSingleStep(0.1)
        self.scale_spin.setMaximumWidth(60)
        self.scale_spin.valueChanged.connect(self._on_changed)
        controls_layout.addWidget(self.scale_spin, 0, 4)

        controls_layout.addWidget(QLabel("Opacity:"), 1, 0)
        self.opacity_spin = QSpinBox()
        self.opacity_spin.setRange(0, 100)
        self.opacity_spin.setValue(100)
        self.opacity_spin.setSuffix("%")
        self.opacity_spin.setMaximumWidth(60)
        self.opacity_spin.valueChanged.connect(self._on_changed)
        controls_layout.addWidget(self.opacity_spin, 1, 1)

        controls_layout.addWidget(QLabel("Rotation:"), 1, 3)
        self.rotation_spin = QSpinBox()
        self.rotation_spin.setRange(0, 359)
        self.rotation_spin.setValue(0)
        self.rotation_spin.setSuffix("°")
        self.rotation_spin.setMaximumWidth(60)
        self.rotation_spin.valueChanged.connect(self._on_changed)
        controls_layout.addWidget(self.rotation_spin, 1, 4)

        controls_layout.addWidget(QLabel("Offset X:"), 2, 0)
        self.offset_x_spin = QDoubleSpinBox()
        self.offset_x_spin.setRange(-0.5, 0.5)
        self.offset_x_spin.setValue(0.0)
        self.offset_x_spin.setSingleStep(0.05)
        self.offset_x_spin.setMaximumWidth(60)
        self.offset_x_spin.valueChanged.connect(self._on_changed)
        controls_layout.addWidget(self.offset_x_spin, 2, 1)

        controls_layout.addWidget(QLabel("Offset Y:"), 2, 3)
        self.offset_y_spin = QDoubleSpinBox()
        self.offset_y_spin.setRange(-0.5, 0.5)
        self.offset_y_spin.setValue(0.0)
        self.offset_y_spin.setSingleStep(0.05)
        self.offset_y_spin.setMaximumWidth(60)
        self.offset_y_spin.valueChanged.connect(self._on_changed)
        controls_layout.addWidget(self.offset_y_spin, 2, 4)

        self.hflip_check = QCheckBox("H-Flip")
        self.hflip_check.stateChanged.connect(self._on_changed)
        controls_layout.addWidget(self.hflip_check, 3, 0, 1, 2)

        self.vflip_check = QCheckBox("V-Flip")
        self.vflip_check.stateChanged.connect(self._on_changed)
        controls_layout.addWidget(self.vflip_check, 3, 3, 1, 2)

        layout.addWidget(controls_widget)

        self._update_icon_preview()

    def _pick_color(self):
        color = QColorDialog.getColor(QColor(self.color_input.text()), self)
        if color.isValid():
            self.color_input.setText(color.name())

    def _on_changed(self):
        self._update_icon_preview()
        self.layer_changed.emit()

    def _update_icon_preview(self):
        try:
            kwargs = self.get_options()
            icon = qta.icon(self.icon_name, **kwargs)
            self.icon_preview.setPixmap(icon.pixmap(QSize(32, 32)))
        except Exception:
            pass

    def get_options(self):
        options = {
            "color": self.color_input.text(),
            "scale_factor": self.scale_spin.value(),
            "opacity": self.opacity_spin.value() / 100.0,
        }

        if self.rotation_spin.value() != 0:
            options["rotated"] = self.rotation_spin.value()

        if self.hflip_check.isChecked():
            options["hflip"] = True

        if self.vflip_check.isChecked():
            options["vflip"] = True

        offset_x = self.offset_x_spin.value()
        offset_y = self.offset_y_spin.value()
        if offset_x != 0 or offset_y != 0:
            options["offset"] = (offset_x, offset_y)

        return options


class StackBuilderPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.all_icons = []
        self.layers = []
        self._load_all_icons()
        self._setup_ui()

    def _load_all_icons(self):
        qta._instance()
        charmap = qta._resource["iconic"].charmap
        for prefix, icons in charmap.items():
            for icon_name in icons.keys():
                self.all_icons.append(f"{prefix}.{icon_name}")
        self.all_icons.sort()

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        splitter = QSplitter(Qt.Horizontal)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        search_group = QGroupBox("Search Icons to Add")
        search_layout = QVBoxLayout(search_group)

        filter_row = QHBoxLayout()

        self.font_filter = QComboBox()
        self.font_filter.addItem("All Fonts", "")
        qta._instance()
        charmap = qta._resource["iconic"].charmap
        font_info = {
            "fa5": "Font Awesome 5 Regular",
            "fa5s": "Font Awesome 5 Solid",
            "fa5b": "Font Awesome 5 Brands",
            "fa6": "Font Awesome 6 Regular",
            "fa6s": "Font Awesome 6 Solid",
            "fa6b": "Font Awesome 6 Brands",
            "ei": "Elusive Icons",
            "mdi": "Material Design Icons 5",
            "mdi6": "Material Design Icons 6",
            "ph": "Phosphor Icons",
            "ri": "Remix Icon",
            "msc": "Microsoft Codicons",
        }
        for prefix in sorted(charmap.keys()):
            display_name = font_info.get(prefix, prefix)
            count = len(charmap[prefix])
            self.font_filter.addItem(f"{display_name} ({count})", prefix)
        self.font_filter.currentIndexChanged.connect(self._filter_icons_immediate)
        filter_row.addWidget(self.font_filter)

        search_layout.addLayout(filter_row)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type to search icons...")
        self.search_input.setClearButtonEnabled(True)
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.setInterval(1000)
        self.search_timer.timeout.connect(self._filter_icons)
        self.search_input.textChanged.connect(self._on_search_changed)
        search_layout.addWidget(self.search_input)

        self.result_count = QLabel(f"Showing {len(self.all_icons)} icons")
        search_layout.addWidget(self.result_count)

        left_layout.addWidget(search_group)

        self.icon_list = IconListWidget()
        self.icon_list.icon_selected.connect(self._add_layer)
        left_layout.addWidget(self.icon_list)

        self._populate_icon_list(self.all_icons)

        hint_label = QLabel("Click an icon to add it as a new layer")
        hint_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        hint_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(hint_label)

        middle_panel = QWidget()
        middle_panel.setMinimumWidth(320)
        middle_layout = QVBoxLayout(middle_panel)
        middle_layout.setContentsMargins(0, 0, 0, 0)

        layers_group = QGroupBox("Layers (bottom to top)")
        layers_group_layout = QVBoxLayout(layers_group)

        self.layers_scroll = QScrollArea()
        self.layers_scroll.setWidgetResizable(True)
        self.layers_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.layers_container = QWidget()
        self.layers_layout = QVBoxLayout(self.layers_container)
        self.layers_layout.setAlignment(Qt.AlignTop)
        self.layers_layout.setSpacing(8)

        self.no_layers_label = QLabel(
            "No layers yet.\nClick icons on the left to add layers."
        )
        self.no_layers_label.setAlignment(Qt.AlignCenter)
        self.no_layers_label.setStyleSheet("color: #7f8c8d; padding: 40px;")
        self.layers_layout.addWidget(self.no_layers_label)

        self.layers_scroll.setWidget(self.layers_container)
        layers_group_layout.addWidget(self.layers_scroll)

        layer_btn_row = QHBoxLayout()

        clear_btn = QPushButton("Clear All")
        clear_btn.setIcon(qta.icon("fa6s.trash", color="#e74c3c"))
        clear_btn.clicked.connect(self._clear_all_layers)
        layer_btn_row.addWidget(clear_btn)

        layer_btn_row.addStretch()
        layers_group_layout.addLayout(layer_btn_row)

        middle_layout.addWidget(layers_group)

        right_panel = QWidget()
        right_panel.setMinimumWidth(280)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        preview_group = QGroupBox("Combined Preview")
        preview_layout = QVBoxLayout(preview_group)

        self.preview_button = QToolButton()
        self.preview_button.setIconSize(QSize(128, 128))
        self.preview_button.setFixedSize(150, 150)
        self.preview_button.setIcon(qta.icon("fa6s.layer-group", color="#7f8c8d"))
        preview_layout.addWidget(self.preview_button, alignment=Qt.AlignCenter)

        self.layer_count_label = QLabel("0 layers")
        self.layer_count_label.setAlignment(Qt.AlignCenter)
        self.layer_count_label.setStyleSheet("font-weight: bold;")
        preview_layout.addWidget(self.layer_count_label)

        right_layout.addWidget(preview_group)

        code_group = QGroupBox("Generated Code")
        code_layout = QVBoxLayout(code_group)

        self.code_text = QLabel("# Add layers to generate code")
        self.code_text.setWordWrap(True)
        self.code_text.setStyleSheet(
            "font-family: monospace; font-size: 10px; color: #7f8c8d; padding: 8px; background-color: #2a2a2a; border-radius: 4px;"
        )
        self.code_text.setTextInteractionFlags(Qt.TextSelectableByMouse)
        code_layout.addWidget(self.code_text)

        copy_code_btn = QPushButton("Copy Code")
        copy_code_btn.setIcon(qta.icon("fa6s.copy", color="#3498db"))
        copy_code_btn.clicked.connect(self._copy_code)
        code_layout.addWidget(copy_code_btn)

        right_layout.addWidget(code_group)

        export_group = QGroupBox("Export")
        export_layout = QVBoxLayout(export_group)

        export_size_row = QHBoxLayout()
        export_size_row.addWidget(QLabel("Size:"))
        self.export_size_combo = QComboBox()
        self.export_size_combo.addItems(["128", "256", "512", "1024", "Custom..."])
        export_size_row.addWidget(self.export_size_combo)
        export_size_row.addStretch()
        export_layout.addLayout(export_size_row)

        export_btn = QPushButton("Export as PNG")
        export_btn.setIcon(qta.icon("fa6s.file-export", color="#27ae60"))
        export_btn.clicked.connect(self._export_stack)
        export_layout.addWidget(export_btn)

        right_layout.addWidget(export_group)

        right_layout.addStretch()

        splitter.addWidget(left_panel)
        splitter.addWidget(middle_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([350, 350, 300])

        main_layout.addWidget(splitter)

    def _populate_icon_list(self, icons):
        self.icon_list.clear()
        for icon_name in icons:
            try:
                item = QListWidgetItem()
                item.setIcon(qta.icon(icon_name))
                item.setText(icon_name.split(".")[-1])
                item.setToolTip(icon_name)
                item.setData(Qt.UserRole, icon_name)
                item.setSizeHint(QSize(80, 60))
                self.icon_list.addItem(item)
            except Exception:
                pass
        self.result_count.setText(f"Showing {self.icon_list.count()} icons")

    def _on_search_changed(self):
        self.search_timer.stop()
        self.search_timer.start()

    def _filter_icons_immediate(self):
        self.search_timer.stop()
        self._filter_icons()

    def _filter_icons(self):
        search_text = self.search_input.text().lower().strip()
        prefix_filter = self.font_filter.currentData()

        if not search_text:
            filtered = []
            for icon_name in self.all_icons:
                if prefix_filter and not icon_name.startswith(prefix_filter + "."):
                    continue
                filtered.append(icon_name)
            self._populate_icon_list(filtered)
            return

        exact_matches = []
        fuzzy_matches = []

        for icon_name in self.all_icons:
            if prefix_filter and not icon_name.startswith(prefix_filter + "."):
                continue

            icon_lower = icon_name.lower()
            short_name = icon_name.split(".")[-1].lower()

            if search_text in icon_lower:
                if short_name == search_text:
                    exact_matches.insert(0, (icon_name, 100))
                elif short_name.startswith(search_text):
                    exact_matches.append((icon_name, 95))
                else:
                    exact_matches.append((icon_name, 90))
            else:
                score = max(
                    fuzz.ratio(search_text, short_name),
                    fuzz.partial_ratio(search_text, short_name),
                )
                if score >= 60:
                    fuzzy_matches.append((icon_name, score))

        exact_matches.sort(key=lambda x: (-x[1], x[0]))
        fuzzy_matches.sort(key=lambda x: (-x[1], x[0]))

        combined = [item[0] for item in exact_matches] + [
            item[0] for item in fuzzy_matches
        ]

        self._populate_icon_list(combined)

    def _add_layer(self, icon_name):
        self.no_layers_label.hide()

        layer_widget = StackLayerWidget(icon_name)
        layer_widget.layer_changed.connect(self._update_preview)
        layer_widget.delete_requested.connect(self._remove_layer)
        layer_widget.move_up_requested.connect(self._move_layer_up)
        layer_widget.move_down_requested.connect(self._move_layer_down)

        self.layers.append(layer_widget)
        self.layers_layout.addWidget(layer_widget)

        self._update_preview()

    def _remove_layer(self, layer_widget):
        if layer_widget in self.layers:
            self.layers.remove(layer_widget)
            self.layers_layout.removeWidget(layer_widget)
            layer_widget.deleteLater()

            if not self.layers:
                self.no_layers_label.show()

            self._update_preview()

    def _move_layer_up(self, layer_widget):
        idx = self.layers.index(layer_widget)
        if idx > 0:
            self.layers.remove(layer_widget)
            self.layers.insert(idx - 1, layer_widget)
            self._rebuild_layer_layout()
            self._update_preview()

    def _move_layer_down(self, layer_widget):
        idx = self.layers.index(layer_widget)
        if idx < len(self.layers) - 1:
            self.layers.remove(layer_widget)
            self.layers.insert(idx + 1, layer_widget)
            self._rebuild_layer_layout()
            self._update_preview()

    def _rebuild_layer_layout(self):
        for i in reversed(range(self.layers_layout.count())):
            item = self.layers_layout.itemAt(i)
            if item.widget() and item.widget() != self.no_layers_label:
                self.layers_layout.removeItem(item)

        for layer in self.layers:
            self.layers_layout.addWidget(layer)

    def _clear_all_layers(self):
        for layer in self.layers[:]:
            self._remove_layer(layer)

    def _update_preview(self):
        self.layer_count_label.setText(
            f"{len(self.layers)} layer{'s' if len(self.layers) != 1 else ''}"
        )

        if not self.layers:
            self.preview_button.setIcon(qta.icon("fa6s.layer-group", color="#7f8c8d"))
            self.code_text.setText("# Add layers to generate code")
            return

        icon_names = [layer.icon_name for layer in self.layers]
        options_list = [layer.get_options() for layer in self.layers]

        try:
            stacked_icon = qta.icon(*icon_names, options=options_list)
            self.preview_button.setIcon(stacked_icon)
        except Exception as e:
            self.code_text.setText(f"# Error: {str(e)}")
            return

        self._update_code_display(icon_names, options_list)

    def _update_code_display(self, icon_names, options_list):
        lines = ["qta.icon("]

        for name in icon_names:
            lines.append(f'    "{name}",')

        lines.append("    options=[")

        for opts in options_list:
            opt_parts = []
            for key, value in opts.items():
                if key == "color":
                    opt_parts.append(f'"color": "{value}"')
                elif key == "offset":
                    opt_parts.append(f'"offset": {value}')
                elif key in ("hflip", "vflip"):
                    opt_parts.append(f'"{key}": True')
                elif key == "opacity" and value != 1.0:
                    opt_parts.append(f'"opacity": {value:.2f}')
                elif key == "scale_factor" and value != 1.0:
                    opt_parts.append(f'"scale_factor": {value:.2f}')
                elif key == "rotated":
                    opt_parts.append(f'"rotated": {value}')
            lines.append("        {" + ", ".join(opt_parts) + "},")

        lines.append("    ]")
        lines.append(")")

        self.code_text.setText("\n".join(lines))

    def _copy_code(self):
        clipboard = QApplication.instance().clipboard()
        clipboard.setText(self.code_text.text())

    def _export_stack(self):
        if not self.layers:
            return

        size_text = self.export_size_combo.currentText()

        if size_text == "Custom...":
            size, ok = QInputDialog.getInt(
                self,
                "Custom Size",
                "Enter size in pixels (will be square):",
                value=256,
                min=16,
                max=4096,
            )
            if not ok:
                return
        else:
            size = int(size_text)

        icon_names = [layer.icon_name for layer in self.layers]
        options_list = [layer.get_options() for layer in self.layers]

        try:
            stacked_icon = qta.icon(*icon_names, options=options_list)
        except Exception:
            return

        default_filename = f"stacked_icon_{size}x{size}.png"

        filepath, _ = QFileDialog.getSaveFileName(
            self, "Export Stacked Icon as PNG", default_filename, "PNG Files (*.png)"
        )

        if filepath:
            if not filepath.lower().endswith(".png"):
                filepath += ".png"
            pixmap = stacked_icon.pixmap(QSize(size, size))
            pixmap.save(filepath, "PNG")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QtAwesome Feature Showcase")
        self.setMinimumSize(1000, 700)
        self.setWindowIcon(qta.icon("fa6s.icons", color="#3498db"))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        nav_frame = QFrame()
        nav_frame.setFixedWidth(200)
        nav_frame.setStyleSheet("background-color: #2c3e50;")
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel("QtAwesome Demo")
        title_label.setStyleSheet(
            "color: white; font-size: 16px; font-weight: bold; padding: 15px;"
        )
        title_label.setAlignment(Qt.AlignCenter)
        nav_layout.addWidget(title_label)

        self.nav_list = QListWidget()
        self.nav_list.setStyleSheet("""
            QListWidget {
                background-color: #2c3e50;
                border: none;
                color: white;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #34495e;
            }
            QListWidget::item:selected {
                background-color: #3498db;
            }
            QListWidget::item:hover {
                background-color: #34495e;
            }
        """)

        nav_items = [
            ("fa6s.font", "Font Showcase"),
            ("fa6s.palette", "Colors"),
            ("fa6s.expand", "Scale & Size"),
            ("fa6s.arrows-rotate", "Transformations"),
            ("fa6s.spinner", "Animations"),
            ("fa6s.layer-group", "Stacked Icons"),
            ("fa6s.image", "IconWidget"),
            ("fa6s.brush", "Themes"),
            ("fa6s.laptop", "Real World Examples"),
            ("fa6s.flask", "Playground"),
            ("fa6s.object-group", "Stack Builder"),
        ]

        for icon_name, text in nav_items:
            item = QListWidgetItem()
            item.setIcon(qta.icon(icon_name, color="white"))
            item.setText(text)
            item.setSizeHint(QSize(200, 45))
            self.nav_list.addItem(item)

        nav_layout.addWidget(self.nav_list)

        self.stack = QStackedWidget()
        self.stack.addWidget(FontShowcasePage())
        self.stack.addWidget(ColorShowcasePage())
        self.stack.addWidget(ScaleShowcasePage())
        self.stack.addWidget(TransformShowcasePage())
        self.stack.addWidget(AnimationShowcasePage())
        self.stack.addWidget(StackedIconsPage())
        self.stack.addWidget(IconWidgetPage())
        self.stack.addWidget(ThemePage())
        self.stack.addWidget(RealWorldPage())
        self.stack.addWidget(PlaygroundPage())
        self.stack.addWidget(StackBuilderPage())

        self.nav_list.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.nav_list.setCurrentRow(0)

        main_layout.addWidget(nav_frame)
        main_layout.addWidget(self.stack)


def main():
    app = QApplication(sys.argv)
    qta.dark(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
