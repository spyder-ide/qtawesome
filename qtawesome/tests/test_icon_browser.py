"""
Tests for QtAwesome Icon Browser.
"""

# Standard library imports
import os

# Third party imports
from qtpy import QtCore, QtWidgets
import pytest

# Local imports
from qtawesome.icon_browser import ExportDialog, IconBrowser
from qtawesome.styles import DEFAULT_DARK_PALETTE


def _select_first_icon(qtbot, browser, search="penguin"):
    """Helper to filter and select the first matching icon."""
    qtbot.keyClicks(browser._lineEditFilter, search)
    qtbot.keyPress(browser._lineEditFilter, QtCore.Qt.Key_Enter)

    model = browser._listView.model()
    selectionModel = browser._listView.selectionModel()
    selectionModel.setCurrentIndex(
        model.index(0, 0), QtCore.QItemSelectionModel.ClearAndSelect
    )
    return browser._getSelectedIconName()


@pytest.fixture
def browser(qtbot):
    browser = IconBrowser()
    browser._updateStyle(DEFAULT_DARK_PALETTE)
    qtbot.add_widget(browser)
    browser.show()
    return browser


def test_browser_init(browser):
    """
    Ensure the browser opens without error
    """

    def close():
        browser.close()

    timer = QtCore.QTimer()
    timer.timeout.connect(close)
    timer.setSingleShot(2000)
    timer.start()


def test_copy(qtbot, browser):
    """
    Ensure the copy UX works
    """
    clipboard = QtWidgets.QApplication.instance().clipboard()

    clipboard.setText("")

    assert clipboard.text() == ""

    # Enter a search term and press enter
    qtbot.keyClicks(browser._lineEditFilter, "penguin")
    qtbot.keyPress(browser._lineEditFilter, QtCore.Qt.Key_Enter)

    # TODO: Figure out how to do this via a qtbot.mouseClick call
    # Select the first item in the list
    model = browser._listView.model()
    selectionModel = browser._listView.selectionModel()
    selectionModel.setCurrentIndex(
        model.index(0, 0), QtCore.QItemSelectionModel.ClearAndSelect
    )

    # Click the copy button
    qtbot.mouseClick(browser._copyButton, QtCore.Qt.LeftButton)

    assert "penguin" in clipboard.text()


def test_filter(qtbot, browser):
    """
    Ensure the filter UX works when searching for `penguin`
    """
    initRowCount = browser._listView.model().rowCount()
    assert initRowCount > 0

    # Enter a search term and click
    qtbot.keyClicks(browser._lineEditFilter, "penguin")
    qtbot.keyPress(browser._lineEditFilter, QtCore.Qt.Key_Enter)

    filteredRowCount = browser._listView.model().rowCount()
    assert initRowCount > filteredRowCount


def test_filter_no_results(qtbot, browser):
    """
    Ensure the filter doesn't show results (the text doesn't match any icon)
    """
    initRowCount = browser._listView.model().rowCount()
    assert initRowCount > 0

    # Enter a search term
    qtbot.keyClicks(browser._lineEditFilter, "I-AM-NOT-penguin-A-penguin")

    # Press Enter to perform the filter
    qtbot.keyPress(browser._lineEditFilter, QtCore.Qt.Key_Enter)

    filteredRowCount = browser._listView.model().rowCount()
    assert filteredRowCount == 0


def test_copy_code(qtbot, browser):
    """
    Ensure the Copy Code action copies a qtawesome.icon() call to clipboard.
    """
    clipboard = QtWidgets.QApplication.instance().clipboard()
    clipboard.setText("")

    iconName = _select_first_icon(qtbot, browser)

    browser._copyIconCode()

    expected = "qtawesome.icon('%s')" % iconName
    assert clipboard.text() == expected


def test_copy_name_action(qtbot, browser):
    """
    Ensure the Copy Name menu action copies the icon name to clipboard.
    """
    clipboard = QtWidgets.QApplication.instance().clipboard()
    clipboard.setText("")

    iconName = _select_first_icon(qtbot, browser)

    # Trigger via the menu action
    browser._copyNameAction.trigger()

    assert clipboard.text() == iconName


def test_export_dialog_init(qtbot, browser):
    """
    Ensure the ExportDialog opens and displays correct defaults.
    """
    iconName = _select_first_icon(qtbot, browser)

    dialog = ExportDialog(iconName, parent=browser)
    qtbot.add_widget(dialog)

    assert dialog.windowTitle() == "Customize Icon"
    assert dialog._iconName == iconName
    assert dialog._scaleSpin.value() == 1.0
    assert dialog._opacitySlider.value() == 100
    assert dialog._rotationSlider.value() == 0
    assert not dialog._hflipCheck.isChecked()
    assert not dialog._vflipCheck.isChecked()
    assert dialog._offsetXSpin.value() == 0.0
    assert dialog._offsetYSpin.value() == 0.0
    assert dialog._sizeSpin.value() == 128


def test_export_dialog_get_kwargs_defaults(qtbot, browser):
    """
    Ensure _getIconKwargs returns empty dict when all values are defaults.
    """
    iconName = _select_first_icon(qtbot, browser)

    dialog = ExportDialog(iconName, parent=browser)
    qtbot.add_widget(dialog)

    kwargs = dialog._getIconKwargs()
    assert kwargs == {}


def test_export_dialog_get_kwargs_custom(qtbot, browser):
    """
    Ensure _getIconKwargs returns correct values for non-default settings.
    """
    iconName = _select_first_icon(qtbot, browser)

    dialog = ExportDialog(iconName, parent=browser)
    qtbot.add_widget(dialog)

    dialog._colorInput.setText("#ff0000")
    dialog._scaleSpin.setValue(2.0)
    dialog._opacitySlider.setValue(50)
    dialog._rotationSlider.setValue(90)
    dialog._hflipCheck.setChecked(True)
    dialog._vflipCheck.setChecked(True)
    dialog._offsetXSpin.setValue(0.1)
    dialog._offsetYSpin.setValue(-0.2)

    kwargs = dialog._getIconKwargs()
    assert kwargs["color"] == "#ff0000"
    assert kwargs["scale_factor"] == 2.0
    assert kwargs["opacity"] == 0.5
    assert kwargs["rotated"] == 90
    assert kwargs["hflip"] is True
    assert kwargs["vflip"] is True
    assert kwargs["offset"] == (0.1, -0.2)


def test_export_dialog_copy_options(qtbot, browser):
    """
    Ensure Copy Options copies a valid Python dict string to clipboard.
    """
    clipboard = QtWidgets.QApplication.instance().clipboard()
    clipboard.setText("")

    iconName = _select_first_icon(qtbot, browser)

    dialog = ExportDialog(iconName, parent=browser)
    qtbot.add_widget(dialog)

    dialog._colorInput.setText("red")
    dialog._copyOptions()

    text = clipboard.text()
    assert "qtawesome.icon(" in text
    assert "'color': 'red'" in text


def test_export_dialog_preview_updates(qtbot, browser):
    """
    Ensure the preview label updates when settings change.
    """
    iconName = _select_first_icon(qtbot, browser)

    dialog = ExportDialog(iconName, parent=browser)
    qtbot.add_widget(dialog)

    # Preview should have a pixmap after init
    assert dialog._previewLabel.pixmap() is not None

    # Change rotation and verify labels update
    dialog._rotationSlider.setValue(45)
    assert dialog._rotationLabel.text() == "45°"

    dialog._opacitySlider.setValue(75)
    assert dialog._opacityLabel.text() == "75%"


def test_export_dialog_do_export(qtbot, browser, tmp_path, monkeypatch):
    """
    Ensure _doExport saves a PNG file when a path is provided.
    """
    iconName = _select_first_icon(qtbot, browser)

    dialog = ExportDialog(iconName, parent=browser)
    qtbot.add_widget(dialog)

    filepath = str(tmp_path / "test_icon.png")
    monkeypatch.setattr(
        QtWidgets.QFileDialog,
        "getSaveFileName",
        staticmethod(lambda *args, **kwargs: (filepath, "PNG Files (*.png)")),
    )

    dialog._doExport()

    assert os.path.exists(filepath)
    assert os.path.getsize(filepath) > 0


def test_context_menu(qtbot, browser, monkeypatch):
    """
    Ensure the context menu contains the expected actions.
    """
    _select_first_icon(qtbot, browser)

    # Capture the menu by replacing _showContextMenu with a version
    # that builds the menu but skips exec_ to avoid blocking on PySide2
    menu = None

    def fakeShowContextMenu(pos):
        nonlocal menu
        if not browser._getSelectedIconName():
            return
        menu = QtWidgets.QMenu(browser)
        menu.addAction(browser._exportAction)
        menu.addAction(browser._copyCodeAction)
        menu.addAction(browser._copyNameAction)
        # Skip menu.exec_() to prevent blocking

    monkeypatch.setattr(browser, "_showContextMenu", fakeShowContextMenu)
    browser._showContextMenu(QtCore.QPoint(10, 10))

    assert menu is not None
    actionTexts = [a.text() for a in menu.actions()]
    assert "Customize &Icon..." in actionTexts
    assert "Copy &Code" in actionTexts
    assert "Copy &Name" in actionTexts


def test_actions_disabled_without_selection(qtbot, browser):
    """
    Ensure menu actions are disabled when no icon is selected.
    """
    assert not browser._exportAction.isEnabled()
    assert not browser._copyCodeAction.isEnabled()
    assert not browser._copyNameAction.isEnabled()


def test_actions_enabled_with_selection(qtbot, browser):
    """
    Ensure menu actions are enabled when an icon is selected.
    """
    _select_first_icon(qtbot, browser)

    assert browser._exportAction.isEnabled()
    assert browser._copyCodeAction.isEnabled()
    assert browser._copyNameAction.isEnabled()


if __name__ == "__main__":
    pytest.main()
