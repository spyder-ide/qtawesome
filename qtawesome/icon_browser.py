
import sys

from qtpy import QtCore, QtGui, QtWidgets

import qtawesome


# TODO: Set icon colour and copy code with color kwarg

VIEW_COLUMNS = 5
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
        self.setMinimumSize(400, 300)
        self.setWindowTitle('QtAwesome Icon Browser')

        qtawesome._instance()
        fontMaps = qtawesome._resource['iconic'].charmap

        iconNames = []
        for fontCollection, fontData in fontMaps.items():
            for iconName in fontData:
                iconNames.append('%s.%s' % (fontCollection, iconName))

        self._filterTimer = QtCore.QTimer(self)
        self._filterTimer.setSingleShot(True)
        self._filterTimer.setInterval(AUTO_SEARCH_TIMEOUT)
        self._filterTimer.timeout.connect(self._updateFilter)

        model = IconModel(self.palette().color(QtGui.QPalette.Text))
        model.setStringList(sorted(iconNames))

        self._proxyModel = QtCore.QSortFilterProxyModel()
        self._proxyModel.setSourceModel(model)
        self._proxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self._listView = IconListView(self)
        self._listView.setUniformItemSizes(True)
        self._listView.setViewMode(QtWidgets.QListView.IconMode)
        self._listView.setModel(self._proxyModel)
        self._listView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._listView.doubleClicked.connect(self._copyIconText)

        self._lineEdit = QtWidgets.QLineEdit(self)
        self._lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self._lineEdit.textChanged.connect(self._triggerDelayedUpdate)
        self._lineEdit.returnPressed.connect(self._triggerImmediateUpdate)

        self._comboBox = QtWidgets.QComboBox(self)
        self._comboBox.setMinimumWidth(75)
        self._comboBox.currentIndexChanged.connect(self._triggerImmediateUpdate)
        self._comboBox.addItems([ALL_COLLECTIONS] + sorted(fontMaps.keys()))

        lyt = QtWidgets.QHBoxLayout()
        lyt.setContentsMargins(0, 0, 0, 0)
        lyt.addWidget(self._comboBox)
        lyt.addWidget(self._lineEdit)

        searchBarFrame = QtWidgets.QFrame(self)
        searchBarFrame.setLayout(lyt)

        self._copyButton = QtWidgets.QPushButton('Copy Name', self)
        self._copyButton.clicked.connect(self._copyIconText)

        lyt = QtWidgets.QVBoxLayout()
        lyt.addWidget(searchBarFrame)
        lyt.addWidget(self._listView)
        lyt.addWidget(self._copyButton)

        frame = QtWidgets.QFrame(self)
        frame.setLayout(lyt)

        self.setCentralWidget(frame)

        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.Key_Return),
            self,
            self._copyIconText,
        )

        self._lineEdit.setFocus()

        geo = self.geometry()
        desktop = QtWidgets.QApplication.desktop()
        screen = desktop.screenNumber(desktop.cursor().pos())
        centerPoint = desktop.screenGeometry(screen).center()
        geo.moveCenter(centerPoint)
        self.setGeometry(geo)

    def _updateFilter(self):
        """
        Update the string used for filtering in the proxy model with the
        current text from the line edit.
        """
        reString = ""

        group = self._comboBox.currentText()
        if group != ALL_COLLECTIONS:
            reString += r"^%s\." % group

        searchTerm = self._lineEdit.text()
        if searchTerm:
            reString += ".*%s.*$" % searchTerm

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
        indexes = self._listView.selectedIndexes()
        if not indexes:
            return

        clipboard = QtWidgets.QApplication.instance().clipboard()
        clipboard.setText(indexes[0].data())


class IconListView(QtWidgets.QListView):
    """
    A QListView that scales it's grid size to ensure the same number of
    columns are always drawn.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

    def resizeEvent(self, event):
        """
        Re-implemented to re-calculate the grid size to provide scaling icons

        Parameters
        ----------
        event : QtCore.QEvent
        """
        width = self.viewport().width() - 30
        # The minus 30 above ensures we don't end up with an item width that
        # can't be drawn the expected number of times across the view without
        # being wrapped. Without this, the view can flicker during resize
        tileWidth = width / VIEW_COLUMNS
        iconWidth = int(tileWidth * 0.8)
        # tileWidth needs to be an integer for setGridSize
        tileWidth = int(tileWidth)

        self.setGridSize(QtCore.QSize(tileWidth, tileWidth))
        self.setIconSize(QtCore.QSize(iconWidth, iconWidth))

        return super().resizeEvent(event)


class IconModel(QtCore.QStringListModel):

    def __init__(self, iconColor):
        super().__init__()
        self._iconColor = iconColor

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
            return qtawesome.icon(iconString, color=self._iconColor)
        return super().data(index, role)


def run():
    """
    Start the IconBrowser and block until the process exits.
    """
    app = QtWidgets.QApplication([])

    browser = IconBrowser()
    browser.show()

    sys.exit(app.exec_())
