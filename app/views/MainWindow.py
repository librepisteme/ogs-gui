from PyQt5.QtCore import QFile, QIODevice
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLabel, QTextEdit
from PyQt5.uic import loadUi, loadUiType
from PyQt5.QtXml import QDomDocument
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

from ..ogsPy.ogsModel import OgsModel,OgsItem
from ..ogsPy.projectModel import OgsProject

MainWindowUI, MainWindowBase = loadUiType('resources/views/MainWindow.ui')


class MainWindow(MainWindowBase, MainWindowUI):
  """Main Window."""

  def __init__(self, parent=None):
    MainWindowBase.__init__(self, parent)
    self.setupUi(self)

    self.model = OgsModel(QDomDocument(), self)
    self.openProject('square.prj')
    self.projectTree.setModel(self.model)

    self.actionOpen.triggered.connect(self.showOpenProjectDialog)
    self.actionSelectElement.triggered.connect(self.selectElement)

  def selectElement(self, element, **args):
    name, value, attributes = self.projectTree.selectedIndexes()
    self.selectedElementName.setText(self.model.data(name, 0))
    self.selectedElementValue.setText(self.model.data(value, 2))

    attributes = self.model.data(attributes, 2)
    if(attributes):
      self.selectedElementAttributes.setRowCount(attributes.length())
      for i in range(attributes.length()):
        self.selectedElementAttributes.setCellvtkWidget(i, 0, QLabel(attributes.item(i).nodeName()))
        self.selectedElementAttributes.setCellWidget(i, 1, QTextEdit(attributes.item(i).nodeValue()))
    else:
      self.selectedElementAttributes.setRowCount(0)

  def showGeometry(self):
    yield

  def openProject(self, filePath):
    # Read File and parse XML
    projectFile = QFile(filePath)

    if projectFile.open(QIODevice.ReadOnly):
      projectDocument = QDomDocument()
      if projectDocument.setContent(projectFile):
        project = OgsModel(projectDocument, self)
        projectBase = OgsProject(projectDocument).projectBase()

        self.projectBase.setModel(projectBase)
        # self.projectTree.setModel(project)
        self.projectPath = filePath
      projectFile.close()

  def showOpenProjectDialog(self):
    print(self)
    filePath, fileType = QFileDialog.getOpenFileName(self, 'Open Project',
      '', 'OpenGeoSys 6 Project (*.prj)')
    self.openProject(filePath)
