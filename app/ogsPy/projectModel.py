from PyQt5.QtCore import QAbstractListModel, QStringListModel

class OgsProjectBase(QAbstractListModel):
    def __init__(self, meshNode, geometryNode, parent=None):
        super().__init__(parent)
        self.meshNode = meshNode
        self.geometryNode = geometryNode

    def rowCount(self, parent):
        if parent.isValid():
            return 2
        return 0

    def data(self, index, role):
        if not index.isValid():
          return None
        return index.data()


class OgsProject():
    def __init__(self, doc):
        print(doc.toString())
        self.mesh = doc.elementsByTagName('mesh').item(0)
        self.geometry = doc.elementsByTagName('geometry').item(0)

    def projectBase(self):
        return OgsProjectBase(self.mesh, self.geometry)

