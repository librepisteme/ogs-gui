import sys
from PyQt5.QtGui import QFontDatabase, QFont, QIcon
from PyQt5.QtCore import QFile, QTextStream, QTranslator, QLocale, QIODevice
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtXml import QDomDocument

from .views.MainWindow import MainWindow
from .ogsPy.ogsModel import OgsModel

from . import resources_rc  # noqa


def main():
  app = QApplication(sys.argv)

  app.setWindowIcon(QIcon(':/icons/app.svg'))

  fontDB = QFontDatabase()
  fontDB.addApplicationFont(':/fonts/Roboto-Regular.ttf')
  app.setFont(QFont('Roboto'))

  f = QFile(':/style.qss')
  f.open(QFile.ReadOnly | QFile.Text)
  app.setStyleSheet(QTextStream(f).readAll())
  f.close()

  translator = QTranslator()
  translator.load(':/translations/' + QLocale.system().name() + '.qm')
  app.installTranslator(translator)

  mw = MainWindow()

  # Read File and parse XML
  filePath = 'square.prj'
  projectFile = QFile(filePath)

  if projectFile.open(QIODevice.ReadOnly):
    projectDocument = QDomDocument()
    if projectDocument.setContent(projectFile):
      newModel = OgsModel(projectDocument, mw)
      mw.model = newModel
      mw.projectTree.setModel(newModel)
      mw.projectTable.setModel(newModel)
      mw.xmlPath = filePath
    projectFile.close()

  mw.show()

  sys.exit(app.exec_())

if __name__ == "__main__":
  main()
