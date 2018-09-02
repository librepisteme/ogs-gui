from PyQt5.QtCore import QAbstractItemModel, QAbstractTableModel, QModelIndex


class OgsItem(object):
    """
        Base Class for OpenGeoSys items
    """

    def __init__(self, node, row, parent=None):
        self.domNode = node
        self.rowNumber = row
        self.parentItem = parent
        self.childItems = {}

    def node(self):
        return self.domNode

    def parent(self):
        return self.parentItem

    """
        When the element is collapsed, childItems don't appear.
        Since we can't transverse the node.childNodes as array,
        we look for the child in the cache object (childItems)
        and use the DOM Node otherwise, adding the child to the
        cache.
    """
    def childByIndex(self, i):
        if i in self.childItems:
            return self.childItems[i]

        if i >= 0 and i < self.domNode.childNodes().count():
            childNode = self.domNode.childNodes().item(i)
            childItem = DomItem(childNode, i, self)
            self.childItems[i] = childItem
            return childItem

        return None

    def row(self):
        return self.rowNumber


"""
    Base Class for OpenGeoSys projects.
    A project consists of one parent item,
    containing multiple child items, etc.
"""

class DomModel(QAbstractTableModel):
    """ XML File as DOM with QT bindings extending QT Abstract Item"""

    def __init__(self, document, parent=None):
        super(DomModel, self).__init__(parent)

        self.domDocument = document
        self.rootItem = DomItem(self.domDocument, 0)

    def columnCount(self):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return None

        # Retrieve node via index
        node = index.internalPointer().node()

        # Here we're only interested in the name
        if index.column() == 0:
            return node.nodeName()

        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        return "Name"

    def index(self, row, column, parent):
        # Return empty index reference on invalid index
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if parent.isValid():
            parentItem = parent.internalPointer()
        else:
            parentItem = self.rootItem

        childItem = parentItem.child(row)

        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, child):
        if not child.isValid():
            return QModelIndex()

        parentItem = child.internalPointer().parent()

        if not parentItem or parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.iternallPointer()
        return parentItem.node().childNodes().count()
