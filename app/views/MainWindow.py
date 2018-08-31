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

    self.projectPath = ""
    self.model = OgsModel(QDomDocument(), self)
    self.projectTree.setModel(self.model)

    self.actionOpen.triggered.connect(self.showOpenProjectDialog)

  def openProject(self, filePath):
    # Read File and parse XML
    projectFile = QFile(filePath)

    if projectFile.open(QIODevice.ReadOnly):
      projectDocument = QDomDocument()

      if projectDocument.setContent(projectFile):
        newProject = OgsModel(projectDocument, self)
        self.project = newProject
        self.projectTree.setModel(newProject)
        self.projectTable.setModel(newProject)
        self.projectPath = filePath
      projectFile.close()

  def showOpenProjectDialog(self):
    print(self)
    filePath, fileType = QFileDialog.getOpenFileName(self, 'Open Project',
      '', 'OpenGeoSys 6 Project (*.prj)')
    self.openProject(filePath)
