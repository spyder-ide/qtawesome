
import sys

from qtpy import QtCore, QtGui, QtWidgets

import qtawesome


# TODO: Set icon colour and copy code with color kwarg

DEFAULT_VIEW_COLUMNS = 5
AUTO_SEARCH_TIMEOUT = 500
ALL_COLLECTIONS = 'All'


class IconBrowser(QtWidgets.QMainWindow):
    """
    A small browser window that allows the user to search through all icons from
    the available version of QtAwesome.  You can also copy the name and python
    code for the currently selected icon.
    """

    def __init__(self):
        super().__init__()

        qtawesome._instance()
        fontMaps = qtawesome._resource['iconic'].charmap

        iconNames = []
        for fontCollection, fontData in fontMaps.items():
            for iconName in fontData:
                iconNames.append('%s.%s' % (fontCollection, iconName))

        self.setMinimumSize(300, 300)
        self.setWindowTitle('QtAwesome Icon Browser')
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

        self._listView = IconListView(self, DEFAULT_VIEW_COLUMNS)
        self._listView.setUniformItemSizes(True)
        self._listView.setViewMode(QtWidgets.QListView.IconMode)
        self._listView.setModel(self._proxyModel)
        self._listView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._listView.doubleClicked.connect(self._copyIconText)
        self._listView.selectionModel().selectionChanged.connect(self._updateNameField)

        toolbar = QtWidgets.QHBoxLayout()

        # filter group
        tbgFont = ToolBarGroup("Filter")
        toolbar.addWidget(tbgFont)
        self._comboFont = QtWidgets.QComboBox(self)
        self._comboFont.setFixedWidth(75)
        self._comboFont.addItems([ALL_COLLECTIONS] + sorted(fontMaps.keys()))
        self._comboFont.currentIndexChanged.connect(self._triggerImmediateUpdate)
        tbgFont.addWidget(self._comboFont)

        self._lineEditFilter = QtWidgets.QLineEdit(self)
        self._lineEditFilter.setFixedWidth(200)
        self._lineEditFilter.setAlignment(QtCore.Qt.AlignLeft)
        self._lineEditFilter.textChanged.connect(self._triggerDelayedUpdate)
        self._lineEditFilter.returnPressed.connect(self._triggerImmediateUpdate)
        tbgFont.addWidget(self._lineEditFilter)

        buttClear = QtWidgets.QToolButton()
        buttClear.setAutoRaise(True)
        buttClear.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        buttClear.setIcon(qtawesome.icon("mdi.alpha-x"))
        buttClear.clicked.connect(self._clearClicked)
        tbgFont.addWidget(buttClear)

        # selected group
        tbgSelected = ToolBarGroup("Selected")
        toolbar.addWidget(tbgSelected)

        self._nameField = QtWidgets.QLineEdit(self)
        self._nameField.setAlignment(QtCore.Qt.AlignCenter)
        self._nameField.setReadOnly(True)
        self._nameField.setFixedWidth(250)
        fnt = self._nameField.font()
        fnt.setFamily("monospace")
        fnt.setBold(True)
        self._nameField.setFont(fnt)
        tbgSelected.addWidget(self._nameField)

        self._copyButton = QtWidgets.QPushButton('Copy Name', self)
        self._copyButton.clicked.connect(self._copyIconText)
        self._copyButton.setDisabled(True)
        tbgSelected.addWidget(self._copyButton)


        toolbar.addStretch(100)

        # Style
        tbgroup = ToolBarGroup("Style")
        toolbar.addWidget(tbgroup)

        self._combo_style = QtWidgets.QComboBox(self)
        self._combo_style.addItem(qtawesome.styles.DEFAULT_DARK_PALETTE, 0)
        self._combo_style.addItem(qtawesome.styles.DEFAULT_LIGHT_PALETTE, 1)
        self._combo_style.currentTextChanged.connect(self._updateStyle)
        tbgroup.addWidget(self._combo_style)


        # Cols across
        tbcols = ToolBarGroup("Columns")
        toolbar.addWidget(tbcols)
        self._combo_cols = QtWidgets.QComboBox(self)
        for idx, no in enumerate([5, 8, 10, 15, 20, 25, 30]):
            self._combo_cols.addItem(str(no), no)
        self._combo_cols.setCurrentIndex(self._combo_cols.findData(DEFAULT_VIEW_COLUMNS))
        tbcols.addWidget(self._combo_cols)
        self._combo_cols.currentTextChanged.connect(self._updateColumns)

        lyt = QtWidgets.QVBoxLayout()
        lyt.addLayout(toolbar)
        lyt.addWidget(self._listView)

        frame = QtWidgets.QFrame(self)
        frame.setLayout(lyt)

        self.setCentralWidget(frame)

        self.setTabOrder(self._comboFont, self._lineEditFilter)
        self.setTabOrder(self._lineEditFilter, self._combo_style)
        self.setTabOrder(self._combo_style, self._listView)
        self.setTabOrder(self._listView, self._nameField)
        self.setTabOrder(self._nameField, self._copyButton)
        self.setTabOrder(self._copyButton, self._comboFont)

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
        self._updateStyle(self._combo_style.currentText())

    def _updateStyle(self, text: str):
        _app = QtWidgets.QApplication.instance()
        if text == qtawesome.styles.DEFAULT_DARK_PALETTE:
            qtawesome.reset_cache()
            qtawesome.dark(_app)
        else:
            qtawesome.reset_cache()
            qtawesome.light(_app)

    def _updateColumns(self):
        self._listView.set_cols(self._combo_cols.currentData())

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

    def _clearClicked(self):
        self._lineEditFilter.clear()

    def _copyIconText(self):
        """
        Copy the name of the currently selected icon to the clipboard.
        """
        indexes = self._listView.selectedIndexes()
        if not indexes:
            return

        clipboard = QtWidgets.QApplication.instance().clipboard()
        clipboard.setText(indexes[0].data())

    def _updateNameField(self):
        """
        Update field to the name of the currently selected icon.
        """
        indexes = self._listView.selectedIndexes()
        if not indexes:
            self._nameField.setText("")
            self._copyButton.setDisabled(True)
            return

        self._nameField.setText(indexes[0].data())
        self._copyButton.setDisabled(False)


class IconListView(QtWidgets.QListView):
    """
    A QListView that scales it's grid size to ensure the same number of
    columns are always drawn.
    """

    def __init__(self, parent, columns):
        super().__init__(parent)
        self._columns = columns
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

    def set_cols(self, cols):
        self._columns = cols
        self._calc_cols()

    def _calc_cols(self):
        """
        re-calculate the grid size to provide scaling icons
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
        self._calc_cols()
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


class ToolBarGroup(QtWidgets.QWidget):
    def __init__(self, title):
        super().__init__()

        vlay = QtWidgets.QVBoxLayout()
        vlay.setContentsMargins(0,0,0,0)
        vlay.setSpacing(2)
        self.setLayout(vlay)

        lbl = QtWidgets.QLabel(title)
        lbl.setFrameShape(QtWidgets.QFrame.Panel)
        lbl.setFrameShadow(QtWidgets.QFrame.Raised)
        vlay.addWidget(lbl)

        self.tbar = QtWidgets.QHBoxLayout()
        self.tbar.setContentsMargins(0, 0, 0, 0)
        self.tbar.setSpacing(2)
        vlay.addLayout(self.tbar)

    def addWidget(self, widget):
        self.tbar.addWidget(widget)




def run():
    """
    Start the IconBrowser and block until the process exits.
    """
    app = QtWidgets.QApplication([])
    qtawesome.dark(app)

    browser = IconBrowser()
    browser.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
