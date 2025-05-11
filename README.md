# NBT Editor

A graphical NBT (Named Binary Tag) editor built with Python and PyQt6. This application allows users to open, view, edit, and save NBT files, which are commonly used in games like Minecraft.

## Features

* **File Operations**:
    * Open NBT files (supports `.nbt`, `.dat`, `.mca`, `.mcr`, `.schematic` formats).
    * Save changes to the current file.
    * Save NBT data to a new file.
    * Drag and drop NBT files to open.
    * Access recently opened files through a dedicated menu.
* **NBT Data Viewing and Editing**:
    * Hierarchical tree view for easy navigation of NBT structures.
    * Edit various NBT tag types including: Compound, List, String, Int, Byte, Short, Long, Float, Double, ByteArray, IntArray, and LongArray.
    * Add new tags to Compounds and Lists.
    * Delete existing tags.
    * Copy and paste tags within the NBT structure.
* **Data Inspection**:
    * Integrated Hex Viewer to inspect binary data within ByteArray, IntArray, and LongArray tags.
* **Search Functionality**:
    * Search for specific tag names or values within the NBT data.
* **Usability**:
    * Undo and Redo functionality to revert or reapply changes.
    * Modern dark theme user interface.
    * Refresh button to reload the current file view.
    * Status bar providing information about selected items and operations.

## Requirements

* Python 3.x
* nbtlib (>=1.20.0)
* PyQt6 (>=6.4.0)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    ```
    (Replace `<your-repository-url>` with the actual URL of your GitHub repository after you've created it.)

2.  **Navigate to the project directory:**
    ```bash
    cd nbt-editor
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    This command will install `nbtlib` and `PyQt6` as specified in the `requirements.txt` file.

## Usage

1.  **Run the application:**
    Execute the main script from the `src` directory:
    ```bash
    python src/main.py
    ```
   
2.  **Using the Editor:**
    * Use the "File" menu or the toolbar icons to open an NBT file.
    * Alternatively, drag and drop an NBT file onto the application window.
    * Navigate the NBT structure using the tree view on the left.
    * Right-click on a tag in the tree view to open a context menu for editing, adding, deleting, copying, or pasting tags.
    * If a ByteArray, IntArray, or LongArray tag is selected, its content will be displayed in the Hex Viewer.
    * Use the search bar or the "Edit" > "Search" menu option to find specific tags.
