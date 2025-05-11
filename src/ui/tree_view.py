from PyQt6.QtWidgets import (QTreeView, QMenu, QInputDialog, 
                            QMessageBox, QApplication)
from PyQt6.QtCore import Qt, QModelIndex
from nbtlib.tag import (Compound, List, String, Int, Byte, 
                       Short, Long, Float, Double, ByteArray, 
                       IntArray, LongArray)
from ui.tree_model import NBTTreeItem  # Changed from relative to absolute import

class NBTTreeView(QTreeView):
    def __init__(self):
        super().__init__()
        self.setAlternatingRowColors(True)
        self.setAnimated(True)
        self.setSortingEnabled(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        # Set selection behavior
        self.setSelectionBehavior(QTreeView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)
        
        # Enable drag and drop
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        
        # Set column widths
        self.setColumnWidth(0, 200)  # Name column
        self.setColumnWidth(1, 300)  # Value column
        
        # Set dark theme specific styles
        self.setStyleSheet("""
            QTreeView {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
            }
            QTreeView::item {
                padding: 4px;
                border-bottom: 1px solid #3d3d3d;
            }
            QTreeView::item:selected {
                background-color: #3d3d3d;
            }
            QTreeView::item:hover {
                background-color: #353535;
            }
            QTreeView::branch {
                background-color: #2d2d2d;
            }
            QTreeView::branch:has-siblings:!adjoins-item {
                border-image: url(vline.png) 0;
            }
            QTreeView::branch:has-siblings:adjoins-item {
                border-image: url(branch-more.png) 0;
            }
            QTreeView::branch:!has-children:!has-siblings:adjoins-item {
                border-image: url(branch-end.png) 0;
            }
            QTreeView::branch:has-children:!has-siblings:closed,
            QTreeView::branch:closed:has-children:has-siblings {
                border-image: none;
                image: url(branch-closed.png);
            }
            QTreeView::branch:open:has-children:!has-siblings,
            QTreeView::branch:open:has-children:has-siblings {
                border-image: none;
                image: url(branch-open.png);
            }
        """)
        
    def show_context_menu(self, position):
        index = self.indexAt(position)
        if not index.isValid():
            return
            
        menu = QMenu()
        
        # Add tag actions with icons
        add_menu = menu.addMenu("Add Tag")
        add_compound = add_menu.addAction("Compound")
        add_list = add_menu.addAction("List")
        add_string = add_menu.addAction("String")
        add_int = add_menu.addAction("Int")
        add_byte = add_menu.addAction("Byte")
        add_short = add_menu.addAction("Short")
        add_long = add_menu.addAction("Long")
        add_float = add_menu.addAction("Float")
        add_double = add_menu.addAction("Double")
        add_byte_array = add_menu.addAction("Byte Array")
        add_int_array = add_menu.addAction("Int Array")
        add_long_array = add_menu.addAction("Long Array")
        
        menu.addSeparator()
        
        # Edit actions
        edit_action = menu.addAction("Edit")
        delete_action = menu.addAction("Delete")
        
        # Copy/Paste actions
        copy_action = menu.addAction("Copy")
        paste_action = menu.addAction("Paste")
        
        # Show menu and handle action
        action = menu.exec(self.viewport().mapToGlobal(position))
        
        if action:
            self.handle_context_menu_action(action, index)
            
    def handle_context_menu_action(self, action, index):
        if action.text() == "Edit":
            self.edit_tag(index)
        elif action.text() == "Delete":
            self.delete_tag(index)
        elif action.text() in ["Compound", "List", "String", "Int", "Byte", 
                             "Short", "Long", "Float", "Double", "Byte Array",
                             "Int Array", "Long Array"]:
            self.add_tag(index, action.text())
        elif action.text() == "Copy":
            self.copy_tag(index)
        elif action.text() == "Paste":
            self.paste_tag(index)
            
    def edit_tag(self, index):
        item = index.internalPointer()
        if not item:
            return
            
        if isinstance(item.data, (Compound, List)):
            return
            
        value, ok = QInputDialog.getText(
            self, "Edit Tag", "Enter new value:", 
            text=str(item.data)
        )
        
        if ok and value:
            try:
                # Convert value to appropriate type
                if isinstance(item.data, String):
                    item.data = String(value)
                elif isinstance(item.data, Int):
                    item.data = Int(int(value))
                elif isinstance(item.data, Byte):
                    item.data = Byte(int(value))
                elif isinstance(item.data, Short):
                    item.data = Short(int(value))
                elif isinstance(item.data, Long):
                    item.data = Long(int(value))
                elif isinstance(item.data, Float):
                    item.data = Float(float(value))
                elif isinstance(item.data, Double):
                    item.data = Double(float(value))
                    
                self.model().dataChanged.emit(index, index)
            except ValueError as e:
                QMessageBox.warning(self, "Error", f"Invalid value: {str(e)}")
                
    def delete_tag(self, index):
        item = index.internalPointer()
        if not item:
            return
            
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this tag?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            parent = item.parent_item
            if parent:
                parent.child_items.remove(item)
                self.model().layoutChanged.emit()
                
    def add_tag(self, parent_index, tag_type):
        parent_item = parent_index.internalPointer()
        if not parent_item:
            return
            
        name, ok = QInputDialog.getText(
            self, "Add Tag", "Enter tag name:"
        )
        
        if not ok:
            return
            
        try:
            if tag_type == "Compound":
                new_tag = Compound()
            elif tag_type == "List":
                new_tag = List()
            elif tag_type == "String":
                new_tag = String("")
            elif tag_type == "Int":
                new_tag = Int(0)
            elif tag_type == "Byte":
                new_tag = Byte(0)
            elif tag_type == "Short":
                new_tag = Short(0)
            elif tag_type == "Long":
                new_tag = Long(0)
            elif tag_type == "Float":
                new_tag = Float(0.0)
            elif tag_type == "Double":
                new_tag = Double(0.0)
            elif tag_type == "Byte Array":
                new_tag = ByteArray([])
            elif tag_type == "Int Array":
                new_tag = IntArray([])
            elif tag_type == "Long Array":
                new_tag = LongArray([])
                
            if isinstance(parent_item.data, Compound):
                parent_item.data[name] = new_tag
                parent_item.child_items.append(NBTTreeItem(new_tag, name, parent_item))
            elif isinstance(parent_item.data, List):
                parent_item.data.append(new_tag)
                parent_item.child_items.append(NBTTreeItem(new_tag, str(len(parent_item.data)-1), parent_item))
                
            self.model().layoutChanged.emit()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add tag: {str(e)}")
            
    def copy_tag(self, index):
        item = index.internalPointer()
        if not item:
            return
            
        # Store the tag data in the clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(str(item.data))
        
    def paste_tag(self, index):
        item = index.internalPointer()
        if not item:
            return
            
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        
        try:
            # Parse the NBT data from the clipboard
            from nbtlib import parse_nbt
            new_tag = parse_nbt(text)
            
            if isinstance(item.data, Compound):
                name, ok = QInputDialog.getText(
                    self, "Paste Tag", "Enter tag name:"
                )
                if ok and name:
                    item.data[name] = new_tag
                    item.child_items.append(NBTTreeItem(new_tag, name, item))
            elif isinstance(item.data, List):
                item.data.append(new_tag)
                item.child_items.append(NBTTreeItem(new_tag, str(len(item.data)-1), item))
                
            self.model().layoutChanged.emit()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to paste tag: {str(e)}")

    def set_model(self, model):
        """Set the tree model and expand the root item."""
        super().setModel(model)
        self.expandToDepth(0) 