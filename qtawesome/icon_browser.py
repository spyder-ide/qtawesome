import sys

from qtpy import QtCore, QtGui, QtWidgets

import qtawesome


DEFAULT_VIEW_COLUMNS = 5
VIEW_COLUMNS_OPTIONS = [5, 8, 10, 15, 20, 25, 30]
AUTO_SEARCH_TIMEOUT = 500
ALL_COLLECTIONS = "All"


class IconBrowser(QtWidgets.QMainWindow):
    """
    A small browser window that allows the user to search through all icons from
    the available version of QtAwesome.  You can also copy the name and python
    code for the currently selected icon.
    """

    def __init__(self):
        super().__init__()

        qtawesome._instance()
        fontMaps = qtawesome._resource["iconic"].charmap

        iconNames = []
        for fontCollection, fontData in fontMaps.items():
            for iconName in fontData:
                iconNames.append("%s.%s" % (fontCollection, iconName))

        self.setMinimumSize(300, 300)
        self.setWindowTitle("QtAwesome Icon Browser")
        self.setWindowIcon(qtawesome.icon("fa5s.icons"))

        self._filterTimer = QtCore.QTimer(self)
        self._filterTimer.setSingleShot(True)
        self._filterTimer.setInterval(AUTO_SEARCH_TIMEOUT)
        self._filterTimer.timeout.connect(self._updateFilter)

        model = IconModel()
        model.setStringList(sorted(iconNames))

        self._proxyModel = QtCore.QSortFilterProxyModel()
        self._proxyModel.setSourceModel(model)
        self._proxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self._listView = IconListView(DEFAULT_VIEW_COLUMNS, parent=self)
        self._listView.setUniformItemSizes(True)
        self._listView.setViewMode(QtWidgets.QListView.IconMode)
        self._listView.setModel(self._proxyModel)
        self._listView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._listView.customContextMenuRequested.connect(self._showContextMenu)
        self._listView.doubleClicked.connect(self._copyIconText)
        self._listView.selectionModel().selectionChanged.connect(self._updateNameField)

        toolbar = QtWidgets.QHBoxLayout()

        # Filter section
        self._comboFont = QtWidgets.QComboBox(self)
        self._comboFont.setToolTip(
            "Select the font prefix whose icons will be included in the filtering."
        )
        self._comboFont.setMaximumWidth(75)
        self._comboFont.addItems([ALL_COLLECTIONS] + sorted(fontMaps.keys()))
        self._comboFont.currentIndexChanged.connect(self._triggerImmediateUpdate)
        toolbar.addWidget(self._comboFont)

        self._lineEditFilter = QtWidgets.QLineEdit(self)
        self._lineEditFilter.setToolTip("Filter icons by name")
        self._lineEditFilter.setMaximumWidth(200)
        self._lineEditFilter.setToolTip("Filter icons by name")
        self._lineEditFilter.setAlignment(QtCore.Qt.AlignLeft)
        self._lineEditFilter.textChanged.connect(self._triggerDelayedUpdate)
        self._lineEditFilter.returnPressed.connect(self._triggerImmediateUpdate)
        self._lineEditFilter.setClearButtonEnabled(True)
        toolbar.addWidget(self._lineEditFilter, stretch=10)

        # Icon name section
        self._nameField = QtWidgets.QLineEdit(self)
        self._nameField.setPlaceholderText(
            "Full identifier of the currently selected icon"
        )
        self._nameField.setAlignment(QtCore.Qt.AlignCenter)
        self._nameField.setReadOnly(True)
        self._nameField.setMaximumWidth(250)
        fnt = self._nameField.font()
        fnt.setFamily("monospace")
        fnt.setBold(True)
        self._nameField.setFont(fnt)
        toolbar.addWidget(self._nameField, stretch=10)

        self._copyButton = QtWidgets.QPushButton("Copy Name", self)
        self._copyButton.setToolTip(
            "Copy selected icon full identifier to the clipboard"
        )
        self._copyButton.clicked.connect(self._copyIconText)
        self._copyButton.setDisabled(True)
        toolbar.addWidget(self._copyButton)
        toolbar.addStretch(1)

        # Style section
        self._comboStyle = QtWidgets.QComboBox(self)
        self._comboStyle.setToolTip(
            "Select color palette for the icons and the icon browser"
        )
        self._comboStyle.addItem(qtawesome.styles.DEFAULT_DARK_PALETTE, 0)
        self._comboStyle.addItem(qtawesome.styles.DEFAULT_LIGHT_PALETTE, 1)
        self._comboStyle.currentTextChanged.connect(self._updateStyle)
        toolbar.addWidget(self._comboStyle)

        # Display (columns number) section
        self._comboColumns = QtWidgets.QComboBox(self)
        self._comboColumns.setToolTip(
            "Select number of columns the icons list is showing"
        )
        for num_columns in VIEW_COLUMNS_OPTIONS:
            self._comboColumns.addItem(str(num_columns), num_columns)
        self._comboColumns.setCurrentIndex(
            self._comboColumns.findData(DEFAULT_VIEW_COLUMNS)
        )
        self._comboColumns.currentTextChanged.connect(self._updateColumns)
        toolbar.addWidget(self._comboColumns)

        # Layout
        lyt = QtWidgets.QVBoxLayout()
        lyt.addLayout(toolbar)
        lyt.addWidget(self._listView)

        frame = QtWidgets.QFrame(self)
        frame.setLayout(lyt)

        self.setCentralWidget(frame)

        # Menu bar
        menuBar = self.menuBar()
        toolsMenu = menuBar.addMenu("&Tools")

        self._exportAction = toolsMenu.addAction("Customize &Icon...")
        self._exportAction.setShortcut(QtGui.QKeySequence("Ctrl+E"))
        self._exportAction.setToolTip("Open the export dialog for the selected icon")
        self._exportAction.setEnabled(False)
        self._exportAction.triggered.connect(self._openExportDialog)

        self._copyCodeAction = toolsMenu.addAction("Copy &Code")
        self._copyCodeAction.setShortcut(QtGui.QKeySequence("Ctrl+Shift+C"))
        self._copyCodeAction.setToolTip(
            "Copy a qtawesome.icon() call for the selected icon to the clipboard"
        )
        self._copyCodeAction.setEnabled(False)
        self._copyCodeAction.triggered.connect(self._copyIconCode)

        self._copyNameAction = toolsMenu.addAction("Copy &Name")
        self._copyNameAction.setShortcut(QtGui.QKeySequence("Ctrl+N"))
        self._copyNameAction.setToolTip("Copy the selected icon name to the clipboard")
        self._copyNameAction.setEnabled(False)
        self._copyNameAction.triggered.connect(self._copyIconText)

        self.setTabOrder(self._comboFont, self._lineEditFilter)
        self.setTabOrder(self._lineEditFilter, self._comboStyle)
        self.setTabOrder(self._comboStyle, self._listView)
        self.setTabOrder(self._listView, self._nameField)
        self.setTabOrder(self._nameField, self._copyButton)
        self.setTabOrder(self._copyButton, self._comboFont)

        # Shortcuts
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.Key_Return),
            self,
            self._copyIconText,
        )
        QtWidgets.QShortcut(
            QtGui.QKeySequence("Ctrl+F"),
            self,
            self._lineEditFilter.setFocus,
        )

        self._lineEditFilter.setFocus()

        geo = self.geometry()

        # QApplication.desktop() has been removed in Qt 6.
        # Instead, QGuiApplication.screenAt(QPoint) is supported
        # in Qt 5.10 or later.
        try:
            screen = QtGui.QGuiApplication.screenAt(QtGui.QCursor.pos())
            centerPoint = screen.geometry().center()
        except AttributeError:
            desktop = QtWidgets.QApplication.desktop()
            screen = desktop.screenNumber(desktop.cursor().pos())
            centerPoint = desktop.screenGeometry(screen).center()

        geo.moveCenter(centerPoint)
        self.setGeometry(geo)
        self._updateStyle(self._comboStyle.currentText())

    def _updateStyle(self, text: str):
        _app = QtWidgets.QApplication.instance()
        if text == qtawesome.styles.DEFAULT_DARK_PALETTE:
            qtawesome.reset_cache()
            qtawesome.dark(_app)
        else:
            qtawesome.reset_cache()
            qtawesome.light(_app)

    def _updateColumns(self):
        self._listView.setColumns(self._comboColumns.currentData())

    def _updateFilter(self):
        """
        Update the string used for filtering in the proxy model with the
        current text from the line edit.
        """
        reString = ""

        group = self._comboFont.currentText()
        if group != ALL_COLLECTIONS:
            reString += r"^%s\." % group

        searchTerm = self._lineEditFilter.text()
        if searchTerm:
            reString += ".*%s.*$" % searchTerm

        # QSortFilterProxyModel.setFilterRegExp has been removed in Qt 6.
        # Instead, QSortFilterProxyModel.setFilterRegularExpression is
        # supported in Qt 5.12 or later.
        try:
            self._proxyModel.setFilterRegularExpression(reString)
        except AttributeError:
            self._proxyModel.setFilterRegExp(reString)

    def _triggerDelayedUpdate(self):
        """
        Reset the timer used for committing the search term to the proxy model.
        """
        self._filterTimer.stop()
        self._filterTimer.start()

    def _triggerImmediateUpdate(self):
        """
        Stop the timer used for committing the search term and update the
        proxy model immediately.
        """
        self._filterTimer.stop()
        self._updateFilter()

    def _copyIconText(self):
        """
        Copy the name of the currently selected icon to the clipboard.
        """
        iconName = self._getSelectedIconName()
        if not iconName:
            return

        clipboard = QtWidgets.QApplication.instance().clipboard()
        clipboard.setText(iconName)

    def _updateNameField(self):
        """
        Update field to the name of the currently selected icon.
        """
        iconName = self._getSelectedIconName()
        if not iconName:
            self._nameField.setText("")
            self._copyButton.setDisabled(True)
            self._exportAction.setEnabled(False)
            self._copyCodeAction.setEnabled(False)
            self._copyNameAction.setEnabled(False)
            return

        self._nameField.setText(iconName)
        self._copyButton.setDisabled(False)
        self._exportAction.setEnabled(True)
        self._copyCodeAction.setEnabled(True)
        self._copyNameAction.setEnabled(True)

    def _getSelectedIconName(self):
        """
        Return the name of the currently selected icon, or None.
        """
        indexes = self._listView.selectedIndexes()
        if not indexes:
            return None
        return indexes[0].data()

    def _openExportDialog(self):
        """
        Open the export dialog for the currently selected icon.
        """
        iconName = self._getSelectedIconName()
        if iconName is None:
            return

        dialog = ExportDialog(iconName, parent=self)
        dialog.exec_()

    def _copyIconCode(self):
        """
        Copy a qtawesome.icon() call for the selected icon to the clipboard.
        """
        iconName = self._getSelectedIconName()
        if iconName is None:
            return

        clipboard = QtWidgets.QApplication.instance().clipboard()
        clipboard.setText("qtawesome.icon('%s')" % iconName)

    def _showContextMenu(self, pos):
        """
        Show a context menu with icon actions at the given position.
        """
        if not self._getSelectedIconName():
            return

        menu = QtWidgets.QMenu(self)
        menu.addAction(self._exportAction)
        menu.addAction(self._copyCodeAction)
        menu.addAction(self._copyNameAction)
        menu.exec_(self._listView.viewport().mapToGlobal(pos))


class ExportDialog(QtWidgets.QDialog):
    """
    A dialog that allows the user to configure icon options (color, scale,
    opacity, rotation, flip, offset), preview the result, export as PNG,
    and copy the configured options as a Python dictionary to the clipboard.
    """

    def __init__(self, iconName, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Customize Icon")
        self.setMinimumWidth(420)
        self._iconName = iconName
        self._setupUi()
        self._updatePreview()

    def _setupUi(self):
        layout = QtWidgets.QVBoxLayout(self)

        # --- Preview ---
        previewGroup = QtWidgets.QGroupBox("Preview")
        previewLayout = QtWidgets.QVBoxLayout(previewGroup)

        self._previewLabel = QtWidgets.QLabel()
        self._previewLabel.setAlignment(QtCore.Qt.AlignCenter)
        self._previewLabel.setMinimumSize(150, 150)
        previewLayout.addWidget(self._previewLabel)

        nameLabel = QtWidgets.QLabel(self._iconName)
        nameLabel.setAlignment(QtCore.Qt.AlignCenter)
        fnt = nameLabel.font()
        fnt.setBold(True)
        nameLabel.setFont(fnt)
        previewLayout.addWidget(nameLabel)

        layout.addWidget(previewGroup)

        # --- Color ---
        colorGroup = QtWidgets.QGroupBox("Color")
        colorLayout = QtWidgets.QHBoxLayout(colorGroup)

        self._colorInput = QtWidgets.QLineEdit()
        self._colorInput.setPlaceholderText("e.g. #3498db or red")
        self._colorInput.textChanged.connect(self._updatePreview)
        colorLayout.addWidget(self._colorInput)

        colorButton = QtWidgets.QPushButton("Pick...")
        colorButton.clicked.connect(self._pickColor)
        colorLayout.addWidget(colorButton)

        layout.addWidget(colorGroup)

        # --- Scale & Opacity ---
        scaleOpacityGroup = QtWidgets.QGroupBox("Scale && Opacity")
        scaleOpacityLayout = QtWidgets.QGridLayout(scaleOpacityGroup)

        scaleOpacityLayout.addWidget(QtWidgets.QLabel("Scale Factor:"), 0, 0)
        self._scaleSpin = QtWidgets.QDoubleSpinBox()
        self._scaleSpin.setRange(0.1, 3.0)
        self._scaleSpin.setValue(1.0)
        self._scaleSpin.setSingleStep(0.1)
        self._scaleSpin.valueChanged.connect(self._updatePreview)
        scaleOpacityLayout.addWidget(self._scaleSpin, 0, 1)

        scaleOpacityLayout.addWidget(QtWidgets.QLabel("Opacity:"), 1, 0)
        self._opacitySlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self._opacitySlider.setRange(0, 100)
        self._opacitySlider.setValue(100)
        self._opacitySlider.valueChanged.connect(self._updatePreview)
        scaleOpacityLayout.addWidget(self._opacitySlider, 1, 1)

        self._opacityLabel = QtWidgets.QLabel("100%")
        self._opacityLabel.setMinimumWidth(45)
        scaleOpacityLayout.addWidget(self._opacityLabel, 1, 2)

        layout.addWidget(scaleOpacityGroup)

        # --- Rotation ---
        rotationGroup = QtWidgets.QGroupBox("Rotation")
        rotationLayout = QtWidgets.QHBoxLayout(rotationGroup)

        self._rotationSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self._rotationSlider.setRange(0, 359)
        self._rotationSlider.setValue(0)
        self._rotationSlider.valueChanged.connect(self._updatePreview)
        rotationLayout.addWidget(self._rotationSlider)

        self._rotationLabel = QtWidgets.QLabel("0°")
        self._rotationLabel.setMinimumWidth(40)
        rotationLayout.addWidget(self._rotationLabel)

        layout.addWidget(rotationGroup)

        # --- Flip ---
        flipGroup = QtWidgets.QGroupBox("Flip")
        flipLayout = QtWidgets.QHBoxLayout(flipGroup)

        self._hflipCheck = QtWidgets.QCheckBox("Horizontal")
        self._hflipCheck.stateChanged.connect(self._updatePreview)
        flipLayout.addWidget(self._hflipCheck)

        self._vflipCheck = QtWidgets.QCheckBox("Vertical")
        self._vflipCheck.stateChanged.connect(self._updatePreview)
        flipLayout.addWidget(self._vflipCheck)

        flipLayout.addStretch()
        layout.addWidget(flipGroup)

        # --- Offset ---
        offsetGroup = QtWidgets.QGroupBox("Offset")
        offsetLayout = QtWidgets.QHBoxLayout(offsetGroup)

        offsetLayout.addWidget(QtWidgets.QLabel("X:"))
        self._offsetXSpin = QtWidgets.QDoubleSpinBox()
        self._offsetXSpin.setRange(-0.5, 0.5)
        self._offsetXSpin.setValue(0.0)
        self._offsetXSpin.setSingleStep(0.05)
        self._offsetXSpin.valueChanged.connect(self._updatePreview)
        offsetLayout.addWidget(self._offsetXSpin)

        offsetLayout.addWidget(QtWidgets.QLabel("Y:"))
        self._offsetYSpin = QtWidgets.QDoubleSpinBox()
        self._offsetYSpin.setRange(-0.5, 0.5)
        self._offsetYSpin.setValue(0.0)
        self._offsetYSpin.setSingleStep(0.05)
        self._offsetYSpin.valueChanged.connect(self._updatePreview)
        offsetLayout.addWidget(self._offsetYSpin)

        offsetLayout.addStretch()
        layout.addWidget(offsetGroup)

        # --- Export size ---
        sizeLayout = QtWidgets.QHBoxLayout()
        sizeLayout.addWidget(QtWidgets.QLabel("Export size (px):"))
        self._sizeSpin = QtWidgets.QSpinBox()
        self._sizeSpin.setRange(16, 1024)
        self._sizeSpin.setValue(128)
        self._sizeSpin.setSingleStep(16)
        sizeLayout.addWidget(self._sizeSpin)
        sizeLayout.addStretch()
        layout.addLayout(sizeLayout)

        # --- Buttons ---
        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addStretch()

        copyOptionsButton = QtWidgets.QPushButton("Copy Options")
        copyOptionsButton.setToolTip(
            "Copy the configured options as a Python dict to the clipboard"
        )
        copyOptionsButton.clicked.connect(self._copyOptions)
        buttonLayout.addWidget(copyOptionsButton)

        exportButton = QtWidgets.QPushButton("Export PNG")
        exportButton.setToolTip("Export the configured icon as a PNG file")
        exportButton.clicked.connect(self._doExport)
        buttonLayout.addWidget(exportButton)

        closeButton = QtWidgets.QPushButton("Close")
        closeButton.clicked.connect(self.reject)
        buttonLayout.addWidget(closeButton)

        layout.addLayout(buttonLayout)

    def _pickColor(self):
        """Open a color picker dialog and set the color input."""
        initial = QtGui.QColor(self._colorInput.text())
        if not initial.isValid():
            initial = QtGui.QColor()
        color = QtWidgets.QColorDialog.getColor(initial, self)
        if color.isValid():
            self._colorInput.setText(color.name())

    def _getIconKwargs(self):
        """
        Build a dict of keyword arguments from the current dialog state.
        Only non-default values are included.
        """
        kwargs = {}

        color = self._colorInput.text().strip()
        if color:
            kwargs["color"] = color

        scaleFactor = self._scaleSpin.value()
        if scaleFactor != 1.0:
            kwargs["scale_factor"] = scaleFactor

        opacity = self._opacitySlider.value() / 100.0
        if opacity != 1.0:
            kwargs["opacity"] = opacity

        rotation = self._rotationSlider.value()
        if rotation != 0:
            kwargs["rotated"] = rotation

        if self._hflipCheck.isChecked():
            kwargs["hflip"] = True

        if self._vflipCheck.isChecked():
            kwargs["vflip"] = True

        offsetX = self._offsetXSpin.value()
        offsetY = self._offsetYSpin.value()
        if offsetX != 0 or offsetY != 0:
            kwargs["offset"] = (offsetX, offsetY)

        return kwargs

    def _updatePreview(self):
        """Update the icon preview and labels from current settings."""
        self._opacityLabel.setText("%d%%" % self._opacitySlider.value())
        self._rotationLabel.setText("%d°" % self._rotationSlider.value())

        kwargs = self._getIconKwargs()
        try:
            icon = qtawesome.icon(self._iconName, **kwargs)
            pixmap = icon.pixmap(QtCore.QSize(128, 128))
            self._previewLabel.setPixmap(pixmap)
        except Exception:
            pass

    def _copyOptions(self):
        """
        Copy the configured icon options as a Python dictionary string
        to the clipboard, formatted for direct use in code.
        """
        kwargs = self._getIconKwargs()

        # Build a human-readable dict representation
        items = []
        for key, value in kwargs.items():
            if isinstance(value, str):
                items.append("    '%s': '%s'" % (key, value))
            elif isinstance(value, tuple):
                items.append("    '%s': %s" % (key, repr(value)))
            elif isinstance(value, bool):
                items.append("    '%s': %s" % (key, repr(value)))
            else:
                items.append("    '%s': %s" % (key, repr(value)))

        if items:
            optionsText = "# qtawesome.icon('%s', **options)\noptions = {\n%s\n}" % (
                self._iconName,
                ",\n".join(items),
            )
        else:
            optionsText = "# qtawesome.icon('%s')  # default options" % self._iconName

        clipboard = QtWidgets.QApplication.instance().clipboard()
        clipboard.setText(optionsText)

    def _doExport(self):
        """Export the configured icon as a PNG file."""
        kwargs = self._getIconKwargs()
        try:
            icon = qtawesome.icon(self._iconName, **kwargs)
        except Exception:
            return

        exportSize = self._sizeSpin.value()
        defaultFilename = "%s_%dx%d.png" % (
            self._iconName.replace(".", "_"),
            exportSize,
            exportSize,
        )

        filepath, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export Icon as PNG", defaultFilename, "PNG Files (*.png)"
        )

        if filepath:
            if not filepath.lower().endswith(".png"):
                filepath += ".png"
            pixmap = icon.pixmap(QtCore.QSize(exportSize, exportSize))
            pixmap.save(filepath, "PNG")


class IconListView(QtWidgets.QListView):
    """
    A QListView that scales it's grid size to ensure the same number of
    columns are always drawn.
    """

    def __init__(self, columns, parent=None):
        super().__init__(parent)
        self._columns = columns
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

    def setColumns(self, cols):
        """
        Set columns number and resize.
        """
        self._columns = cols
        self._resize()

    def _resize(self):
        """
        Set grid and icon size taking into account the number of columns.
        """

        width = self.viewport().width() - 30
        # The minus 30 above ensures we don't end up with an item width that
        # can't be drawn the expected number of times across the view without
        # being wrapped. Without this, the view can flicker during resize
        tileWidth = width / self._columns
        iconWidth = int(tileWidth * 0.8)
        # tileWidth needs to be an integer for setGridSize
        tileWidth = int(tileWidth)

        self.setGridSize(QtCore.QSize(tileWidth, tileWidth))
        self.setIconSize(QtCore.QSize(iconWidth, iconWidth))

    def resizeEvent(self, event):
        """
        Re-implemented to resize view following number of columns available.
        """
        self._resize()
        return super().resizeEvent(event)


class IconModel(QtCore.QStringListModel):
    def __init__(self):
        super().__init__()

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role):
        """
        Re-implemented to return the icon for the current index.

        Parameters
        ----------
        index : QtCore.QModelIndex
        role : int

        Returns
        -------
        Any
        """
        if role == QtCore.Qt.DecorationRole:
            iconString = self.data(index, role=QtCore.Qt.DisplayRole)
            return qtawesome.icon(iconString)
        return super().data(index, role)


def run():
    """
    Start the IconBrowser and block until the process exits.
    """
    app = QtWidgets.QApplication([])
    qtawesome.dark(app)

    browser = IconBrowser()
    browser.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
