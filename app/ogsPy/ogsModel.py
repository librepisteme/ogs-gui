from PyQt5.QtCore import Qt, QAbstractItemModel, QFile, QIODevice, QModelIndex
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QTreeView
from PyQt5.QtXml import QDomDocument
from PyQt5.QtXmlPatterns import QXmlSchema, QXmlSchemaValidator

class OgsItem(object):
    def __init__(self, node, row, parent=None):
        self.domNode = node
        # Record the item's location within its parent.
        self.rowNumber = row
        self.parentItem = parent
        self.childItems = {}

    def name(self):
        return self.domNode.nodeName()

    def node(self):
        return self.domNode

    def parent(self):
        return self.parentItem

    def child(self, i):
        if i in self.childItems:
            return self.childItems[i]

        if i >= 0 and i < self.domNode.childNodes().count():
            childNode = self.domNode.childNodes().item(i)
            childItem = OgsItem(childNode, i, self)

            self.childItems[i] = childItem
            return childItem

        return None

    def row(self):
        return self.rowNumber

class OgsModel(QAbstractItemModel):
    def __init__(self, document, parent=None):
        super(OgsModel, self).__init__(parent)
        self.domDocument = document
        self.rootItem = OgsItem(self.domDocument, 0)

        # Read project schema xsd file and create name pool
        schema_file = QFile('OpenGeoSysProject.xsd')
        schema_file.open(QIODevice.ReadOnly)
        project_schema = QXmlSchema()
        project_schema.load(schema_file)
        self.namePool = project_schema.namePool()
        print(self.namePool)

    def columnCount(self, parent):
        return 4

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()

        node = item.node()
        attributes = []
        attributeMap = node.attributes()

        if index.column() == 0:
            return node.nodeName()

        elif index.column() == 1:
            value = node.nodeValue()
            if value is None:
                return ''

            return ' '.join(node.nodeValue().split('\n'))


        elif index.column() == 2:
            for i in range(0, attributeMap.count()):
                attribute = attributeMap.item(i)
                attributes.append(attribute.nodeName() + '="' +
                                  attribute.nodeValue() + '"')

            return " ".join(attributes)
        elif index.column() == 3:
            return node.nodeType()

        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return "Name"

            if section == 1:
                return "Value"

            if section == 2:
                return "Attributes"

            if section == 3:
                return "Type"

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, child):
        if not child.isValid():
            return QModelIndex()

        childItem = child.internalPointer()
        parentItem = childItem.parent()

        if not parentItem or parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.node().childNodes().count()

def createProject(document):
    # Read project schema xsd file
    schema_file = QFile('OpenGeoSysProject.xsd')
    schema_file.open(QIODevice.ReadOnly)
    project_schema = QXmlSchema()
    project_schema.load(schema_file)

    if project_schema.isValid():
        validator = QXmlSchemaValidator(project_schema)
    else:
        validator = None
    return OrgModel(document, parent=0, validator=validator)
