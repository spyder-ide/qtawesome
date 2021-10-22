"""
QT MODERN

MIT License

Copyright (c) 2017 Gerard Marull-Paretas <gerardmarull@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from qtpy.QtGui import QPalette, QColor


def dark(app):
    """
    Apply dark theme to the Qt application instance.

    Args:
        app (QApplication): QApplication instance.
    """

    dark_palette = QPalette()

    # base
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(180, 180, 180))
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.Light, QColor(180, 180, 180))
    dark_palette.setColor(QPalette.ColorRole.Midlight, QColor(90, 90, 90))
    dark_palette.setColor(QPalette.ColorRole.Dark, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.ColorRole.Text, QColor(180, 180, 180))
    dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(180, 180, 180))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(180, 180, 180))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42))
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.Shadow, QColor(20, 20, 20))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(180, 180, 180))
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(56, 252, 196))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(66, 66, 66))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(180, 180, 180))
    dark_palette.setColor(QPalette.ColorRole.LinkVisited, QColor(80, 80, 80))

    # disabled
    dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText,
                         QColor(127, 127, 127))
    dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text,
                         QColor(127, 127, 127))
    dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText,
                         QColor(127, 127, 127))
    dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Highlight,
                         QColor(80, 80, 80))
    dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.HighlightedText,
                         QColor(127, 127, 127))

    app.style().unpolish(app)
    app.setPalette(dark_palette)

    app.setStyle('Fusion')


def light(app):
    """
    Apply light theme to the Qt application instance.

    Args:
        app (QApplication): QApplication instance.
    """

    light_palette = QPalette()

    # base
    light_palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    light_palette.setColor(QPalette.ColorRole.Light, QColor(180, 180, 180))
    light_palette.setColor(QPalette.ColorRole.Midlight, QColor(200, 200, 200))
    light_palette.setColor(QPalette.ColorRole.Dark, QColor(225, 225, 225))
    light_palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.BrightText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.Base, QColor(237, 237, 237))
    light_palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    light_palette.setColor(QPalette.ColorRole.Shadow, QColor(20, 20, 20))
    light_palette.setColor(QPalette.ColorRole.Highlight, QColor(76, 163, 224))
    light_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.Link, QColor(0, 162, 232))
    light_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(225, 225, 225))
    light_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(240, 240, 240))
    light_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.LinkVisited, QColor(222, 222, 222))

    # disabled
    light_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText,
                          QColor(115, 115, 115))
    light_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text,
                          QColor(115, 115, 115))
    light_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText,
                          QColor(115, 115, 115))
    light_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Highlight,
                          QColor(190, 190, 190))
    light_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.HighlightedText,
                          QColor(115, 115, 115))

    app.style().unpolish(app)
    app.setPalette(light_palette)

    app.setStyle('Fusion')
