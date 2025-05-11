from PyQt6.QtCore import QAbstractItemModel, QModelIndex, Qt, QObject
from nbtlib.tag import Base, Compound, List, String, Int, Byte, Short, Long, Float, Double, ByteArray, IntArray, LongArray

class NBTTreeItem:
    def __init__(self, data, name="", parent=None):
        self.parent_item = parent
        self.name = name
        self.data = data
        self.child_items = []
        self._setup_children()

    def _setup_children(self):
        if isinstance(self.data, Compound):
            for key, value in self.data.items():
                self.child_items.append(NBTTreeItem(value, key, self))
        elif isinstance(self.data, List):
            for i, value in enumerate(self.data):
                self.child_items.append(NBTTreeItem(value, str(i), self))

    def child(self, row):
        return self.child_items[row] if 0 <= row < len(self.child_items) else None

    def childCount(self):
        return len(self.child_items)

    def row(self):
        if self.parent_item:
            return self.parent_item.child_items.index(self)
        return 0

    @property
    def value(self):
        if isinstance(self.data, (Compound, List)):
            return f"{type(self.data).__name__} ({len(self.data)} items)"
        return str(self.data)

class NBTTreeModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.root_item = None

    def set_root(self, nbt_data):
        self.beginResetModel()
        self.root_item = NBTTreeItem(nbt_data)
        self.endResetModel()

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item.parent_item

        if parent_item == self.root_item:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()

        return parent_item.childCount()

    def columnCount(self, parent=QModelIndex()):
        return 2  # Name and Value columns

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        item = index.internalPointer()
        
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return item.name
            elif index.column() == 1:
                return item.value
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return ["Name", "Value"][section]
        return None 