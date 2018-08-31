from PyQt5.QtCore import QFile, QIODevice
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.uic import loadUi, loadUiType
from PyQt5.QtXml import QDomDocument

from ..ogsPy.ogsModel import OgsModel

MainWindowUI, MainWindowBase = loadUiType('resources/views/MainWindow.ui')


class MainWindow(MainWindowBase, MainWindowUI):
  """Main Window."""

  def __init__(self, parent=None):
    MainWindowBase.__init__(self, parent)
    self.setupUi(self)

    self.xmlPath = ""
    self.model = OgsModel(QDomDocument(), self)
    self.projectTree.setModel(self.model)

    self.actionOpen.triggered.connect(self.showOpenFileDialog)

  def showOpenFileDialog(self):
    filePath, fileType = QFileDialog.getOpenFileName(self, 'Open Project',
        '', 'OpenGeoSys 6 Project (*.prj)')

    # Read File and parse XML
    projectFile = QFile(filePath)

    if projectFile.open(QIODevice.ReadOnly):
      projectDocument = QDomDocument()

      if projectDocument.setContent(projectFile):
        newModel = OgsModel(projectDocument, self)
        self.model = newModel
        self.projectTree.setModel(newModel)
        self.projectTable.setModel(newModel)
        self.xmlPath = filePath

      projectFile.close()
