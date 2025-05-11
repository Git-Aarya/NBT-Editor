from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTreeView, QMenuBar, QMenu, QFileDialog, QMessageBox,
    QDockWidget, QToolBar, QStatusBar, QLineEdit, QPushButton, QSplitter
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from ui.tree_view import NBTTreeView
from ui.hex_viewer import HexViewer
from ui.search_dialog import SearchDialog
from core.nbt_handler import NBTHandler
from nbtlib.tag import ByteArray, IntArray, LongArray

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NBT Editor")
        self.setMinimumSize(1000, 700)
        
        self.nbt_handler = NBTHandler()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        
        tree_container = QWidget()
        tree_layout = QVBoxLayout(tree_container)
        tree_layout.setContentsMargins(0, 0, 0, 0)
        
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search tags...")
        self.search_input.textChanged.connect(self.filter_tree)
        search_layout.addWidget(self.search_input)
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_view)
        search_layout.addWidget(refresh_button)
        
        tree_layout.addLayout(search_layout)
        
        self.tree_view = NBTTreeView()
        tree_layout.addWidget(self.tree_view)
        
        splitter.addWidget(tree_container)
        
        self.hex_viewer = HexViewer()
        hex_dock = QDockWidget("Hex Viewer", self)
        hex_dock.setWidget(self.hex_viewer)
        hex_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable | 
                           QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, hex_dock)
        
        splitter.setSizes([700, 300])
        
        self.create_menu_bar()
        self.create_toolbar()
        
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        self.setAcceptDrops(True)
        
        self.tree_view.clicked.connect(self.on_tree_item_clicked)
        self.tree_view.expanded.connect(self.on_tree_item_expanded)
        self.tree_view.collapsed.connect(self.on_tree_item_collapsed)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; }
            QWidget { background-color: #1e1e1e; color: #ffffff; }
            QTreeView {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: #ffffff;
            }
            QTreeView::item {
                padding: 4px;
                border-bottom: 1px solid #3d3d3d;
            }
            QTreeView::item:selected { background-color: #3d3d3d; }
            QTreeView::item:hover { background-color: #353535; }
            QLineEdit {
                padding: 5px;
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: #ffffff;
            }
            QPushButton {
                padding: 5px 10px;
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: #ffffff;
            }
            QPushButton:hover { background-color: #3d3d3d; }
            QPushButton:pressed { background-color: #4d4d4d; }
            QMenuBar {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QMenuBar::item {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QMenuBar::item:selected { background-color: #3d3d3d; }
            QMenu {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected { background-color: #3d3d3d; }
            QToolBar {
                background-color: #2d2d2d;
                border: none;
            }
            QToolBar::separator {
                background-color: #3d3d3d;
                width: 1px;
                margin: 0 5px;
            }
            QStatusBar {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QDockWidget {
                color: #ffffff;
            }
            QDockWidget::title {
                background-color: #2d2d2d;
                padding: 5px;
            }
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 12px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #3d3d3d;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover { background-color: #4d4d4d; }
            QScrollBar:horizontal {
                background-color: #2d2d2d;
                height: 12px;
                margin: 0;
            }
            QScrollBar::handle:horizontal {
                background-color: #3d3d3d;
                min-width: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal:hover { background-color: #4d4d4d; }
            QHeaderView::section {
                background-color: #2d2d2d;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #3d3d3d;
            }
        """)

    def create_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        
        open_action = file_menu.addAction("Open")
        open_action.triggered.connect(self.open_file)
        
        save_action = file_menu.addAction("Save")
        save_action.triggered.connect(self.save_file)
        
        save_as_action = file_menu.addAction("Save As")
        save_as_action.triggered.connect(self.save_file_as)
        
        file_menu.addSeparator()
        
        self.recent_menu = file_menu.addMenu("Recent Files")
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        edit_menu = menubar.addMenu("Edit")
        search_action = edit_menu.addAction("Search")
        search_action.triggered.connect(self.show_search_dialog)
        
        view_menu = menubar.addMenu("View")
        toggle_hex_action = view_menu.addAction("Toggle Hex Viewer")
        toggle_hex_action.triggered.connect(self.toggle_hex_viewer)

    def create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        search_action = QAction("Search", self)
        search_action.setShortcut("Ctrl+F")
        search_action.triggered.connect(self.show_search_dialog)
        toolbar.addAction(search_action)
        
        toolbar.addSeparator()
        
        toggle_hex_action = QAction("Toggle Hex Viewer", self)
        toggle_hex_action.setCheckable(True)
        toggle_hex_action.setChecked(True)
        toggle_hex_action.triggered.connect(self.toggle_hex_viewer)
        toolbar.addAction(toggle_hex_action)

    def filter_tree(self, text):
        pass

    def refresh_view(self):
        if self.nbt_handler.current_file:
            self.open_file(self.nbt_handler.current_file)

    def on_tree_item_expanded(self, index):
        item = index.internalPointer()
        if item:
            self.statusBar.showMessage(f"Expanded: {item.name}")

    def on_tree_item_collapsed(self, index):
        item = index.internalPointer()
        if item:
            self.statusBar.showMessage(f"Collapsed: {item.name}")

    def on_tree_item_clicked(self, index):
        item = index.internalPointer()
        if not item:
            return
            
        if isinstance(item.data, (ByteArray, IntArray, LongArray)):
            self.hex_viewer.display_data(bytes(item.data))
        else:
            self.hex_viewer.display_data(None)
            
        self.statusBar.showMessage(f"Type: {type(item.data).__name__}")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        if files:
            self.open_file(files[0])

    def open_file(self, file_name=None):
        if file_name is None:
            file_name, _ = QFileDialog.getOpenFileName(
                self,
                "Open NBT File",
                "",
                "NBT Files (*.nbt *.dat *.mca *.mcr *.schematic);;All Files (*.*)"
            )
        
        if file_name:
            try:
                self.nbt_handler.load_file(file_name)
                self.tree_view.setModel(self.nbt_handler.get_tree_model())
                self.tree_view.expandToDepth(0)
                self.add_recent_file(file_name)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file: {str(e)}")

    def add_recent_file(self, file_name):
        action = QAction(file_name, self)
        action.triggered.connect(lambda: self.open_file(file_name))
        self.recent_menu.addAction(action)
        
        if self.recent_menu.actions():
            self.recent_menu.removeAction(self.recent_menu.actions()[0])

    def save_file(self):
        if not self.nbt_handler.current_file:
            self.save_file_as()
            return
            
        try:
            self.nbt_handler.save_file()
            self.statusBar.showMessage("File saved successfully", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")

    def save_file_as(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save NBT File",
            "",
            "NBT Files (*.nbt *.dat);;All Files (*.*)"
        )
        
        if file_name:
            try:
                self.nbt_handler.save_file_as(file_name)
                self.statusBar.showMessage("File saved successfully", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")

    def show_search_dialog(self):
        dialog = SearchDialog(self)
        if dialog.exec():
            search_text = dialog.search_text.text()
            search_type = dialog.search_type.currentText()
            self.search_nbt(search_text, search_type)

    def search_nbt(self, text, search_type):
        pass

    def toggle_hex_viewer(self):
        hex_dock = self.findChild(QDockWidget, "Hex Viewer")
        if hex_dock:
            hex_dock.setVisible(not hex_dock.isVisible()) 