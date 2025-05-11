from nbtlib import nbt
from PyQt6.QtCore import QAbstractItemModel, QModelIndex, Qt
from ui.tree_model import NBTTreeModel
import copy

class NBTHandler:
    def __init__(self):
        self.current_file = None
        self.nbt_data = None
        self.tree_model = NBTTreeModel()
        self.undo_stack = []
        self.redo_stack = []
        
    def load_file(self, file_path):
        """Load an NBT file."""
        self.current_file = file_path
        self.nbt_data = nbt.load(file_path)
        self.tree_model.set_root(self.nbt_data)
        self.undo_stack.clear()
        self.redo_stack.clear()
        
    def save_file(self):
        """Save the current NBT data to the current file."""
        if not self.current_file or not self.nbt_data:
            raise ValueError("No file is currently open")
        self.nbt_data.save(self.current_file)
        
    def save_file_as(self, file_path):
        """Save the current NBT data to a new file."""
        if not self.nbt_data:
            raise ValueError("No NBT data to save")
        self.current_file = file_path
        self.nbt_data.save(file_path)
        
    def get_tree_model(self):
        """Return the tree model."""
        return self.tree_model
        
    def push_undo(self):
        """Save current state to undo stack."""
        if self.nbt_data:
            self.undo_stack.append(copy.deepcopy(self.nbt_data))
            self.redo_stack.clear()
            
    def undo(self):
        """Undo last change."""
        if self.undo_stack:
            self.redo_stack.append(copy.deepcopy(self.nbt_data))
            self.nbt_data = self.undo_stack.pop()
            self.tree_model.set_root(self.nbt_data)
            
    def redo(self):
        """Redo last undone change."""
        if self.redo_stack:
            self.undo_stack.append(copy.deepcopy(self.nbt_data))
            self.nbt_data = self.redo_stack.pop()
            self.tree_model.set_root(self.nbt_data) 