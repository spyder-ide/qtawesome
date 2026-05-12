from __future__ import annotations

from qtpy import QtCore
from qtpy.QtCore import QTimer
from qtpy.QtGui import QPainter
from qtpy.QtWidgets import QWidget


class Spin:
    def __init__(
        self,
        parent_widget: QWidget,
        interval: int = 10,
        step: int = 1,
        autostart: bool = True,
    ) -> None:
        self.parent_widget = parent_widget
        self.interval = interval
        self.step = step
        self.autostart = autostart

        self.info: dict[QWidget, tuple[QTimer, int, int]] = {}

    def _update(self):
        if self.parent_widget in self.info:
            timer, angle, step = self.info[self.parent_widget]

            if angle >= 360:
                angle = 0

            angle += step
            self.info[self.parent_widget] = timer, angle, step
            self.parent_widget.update()

    def setup(
        self, icon_painter: object, painter: QPainter, rect: QtCore.QRect
    ) -> None:
        if self.parent_widget not in self.info:
            timer = QTimer(self.parent_widget)
            timer.timeout.connect(self._update)
            self.info[self.parent_widget] = [timer, 0, self.step]
            if self.autostart:
                timer.start(self.interval)
        else:
            timer, angle, self.step = self.info[self.parent_widget]
            x_center = rect.x() + rect.width() * 0.5
            y_center = rect.y() + rect.height() * 0.5
            painter.translate(x_center, y_center)
            painter.rotate(angle)
            painter.translate(-x_center, -y_center)

    def start(self) -> None:
        if self.parent_widget in self.info:
            timer: QTimer = self.info[self.parent_widget][0]
            timer.start(self.interval)

    def stop(self) -> None:
        if self.parent_widget in self.info:
            timer: QTimer = self.info[self.parent_widget][0]
            timer.stop()


class Pulse(Spin):
    def __init__(self, parent_widget: QWidget, autostart: bool = True) -> None:
        super().__init__(parent_widget, interval=300, step=45, autostart=autostart)
