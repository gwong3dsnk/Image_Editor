import sys
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import *
from load_images_func import LoadImages


class GuiMain(QWidget):
    """
    The UI class.  Sets up the GUI for the Image Editing application.
    """
    def __init__(self):
        super().__init__()
        # print(PySide6.__version__)

        self.setWindowTitle("Photo Editor")
        self.setMinimumSize(500, 350)

        # Instantiate func classes to access data logic
        self.load_images = LoadImages()

        # Create the top menu bar
        self.menu_bar = QMenuBar(self)
        self.create_menu_bar()

        # Create the window tab objects
        self.tab_load_images = QWidget()
        self.tab_edit_images = QWidget()
        self.tab_export_images = QWidget()
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.tab_load_images, "Tab 1")
        self.tab_widget.addTab(self.tab_edit_images, "Tab 2")
        self.tab_widget.addTab(self.tab_export_images, "Tab 3")

        # Initialize image load widgets
        self.button_browse_image_files = QPushButton(text="Browse File(s)")
        self.button_browse_image_files.clicked.connect(self.populate_image_list_widget)
        self.button_browse_image_folder = QPushButton(text="Browse Folder")
        self.button_browse_image_folder.clicked.connect(LoadImages.browse_for_folder)
        self.image_url_list = QListWidget()
        self.image_url_list.setFixedSize(500, 250)
        self.button_clear_url_list = QPushButton(text="Clear File(s)")
        self.button_clear_url_list.clicked.connect(self.clean_url_list)
        self.button_remove_selected_url = QPushButton(text="Remove Selected File(s)")
        self.button_remove_selected_url.clicked.connect(LoadImages.remove_selected_urls)

        # Initialize image edit widgets
        self.label_image_preview = QLabel()
        self.label_image_preview.setFixedSize(500, 400)
        self.label_image_preview.setStyleSheet("background-color: black;")
        self.line_edit_x_res = QLineEdit()
        self.line_edit_x_res.setPlaceholderText("New X Res")
        self.line_edit_y_res = QLineEdit()
        self.line_edit_y_res.setPlaceholderText("New Y Res")
        self.line_edit_contrast = QLineEdit()
        self.line_edit_contrast.setPlaceholderText("i.e. 1.3 for 30%")
        self.line_edit_rotate = QLineEdit()
        self.line_edit_rotate.setPlaceholderText("Enter rotation degrees")
        self.line_edit_sharpness = QLineEdit()
        self.line_edit_sharpness.setPlaceholderText("0 b/w, 1.0 orig, 1.0+ sharpen")
        self.line_edit_brightness = QLineEdit()
        self.line_edit_brightness.setPlaceholderText("0 b, 1.0 orig, 1.0+ brighten")
        self.combobox_rotation = QComboBox()
        self.combobox_rotation.addItem("Degrees")
        self.combobox_rotation.addItem("90")
        self.combobox_rotation.addItem("180")
        self.combobox_rotation.addItem("270")
        self.combobox_active_image = QComboBox()
        self.combobox_active_image.addItem("Select an Image to Edit")
        self.button_toggle_preview = QPushButton(text="Toggle Image Changes")
        self.checkbox_apply_all_images = QCheckBox()
        self.checkbox_apply_all_images.setChecked(True)

        # Initialize image export widgets
        self.line_edit_export_dir = QLineEdit()
        self.line_edit_export_dir.setPlaceholderText("Browse to export directory")
        self.line_edit_export_dir.setReadOnly(True)
        self.line_edit_export_dir.setStyleSheet("background-color: lightgray;")
        self.button_browse_export_dir = QPushButton(text="Browse to Export Dir")
        self.button_export_files = QPushButton(text="Export File(s)")
        self.combobox_image_format = QComboBox()
        self.combobox_image_format.addItem("Choose Image Format")
        self.combobox_image_format.addItem("BMP")
        self.combobox_image_format.addItem("GIF")
        self.combobox_image_format.addItem("JPEG")
        self.combobox_image_format.addItem("PNG")
        self.line_edit_prefix = QLineEdit()
        self.line_edit_prefix.setPlaceholderText("Enter Prefix")
        self.line_edit_suffix = QLineEdit()
        self.line_edit_suffix.setPlaceholderText("Enter Suffix")
        self.line_edit_filename = QLineEdit()
        self.line_edit_filename.setPlaceholderText("Enter File Name")
        self.line_edit_filename.setReadOnly(True)
        self.line_edit_filename.setStyleSheet("background-color: lightgray;")
        self.checkbox_use_orig_filename = QCheckBox()
        self.checkbox_use_orig_filename.setChecked(True)
        self.checkbox_append_number = QCheckBox()
        self.checkbox_append_number.setChecked(False)

        # Populate the window tab objects with widgets
        self.init_tab_load_images()
        self.init_tab_edit_images()
        self.init_tab_export_images()

        # Add the tab widget to a main layout and set the layout so it shows up
        main_layout = QGridLayout()
        main_layout.addWidget(self.tab_widget, 0, 0)
        self.setLayout(main_layout)
        main_layout.setMenuBar(self.menu_bar)

    def create_menu_bar(self):
        """
        Create the menu bar and subsequent menu items
        :return:
        """
        # Create the menu
        file_menu = QMenu("File", self)

        # Create the menu actions
        exit_action = QtGui.QAction("Exit", self)

        # Create the function call when the action is triggered.
        exit_action.triggered.connect(self.exit_action_triggered)

        # Add the action to the menu
        file_menu.addAction(exit_action)

        # Add the menu to the parent QMenuBar
        self.menu_bar.addMenu(file_menu)

    def exit_action_triggered(self):
        """
        Exit the application
        :return:
        """
        sys.exit()

    def init_tab_load_images(self):
        """
        Initialize the grid layout for the Load Image tab and add the widgets.  Then name the tab and
        add the grid to the tab.
        :return:
        """
        layout_load_images = QGridLayout(self)
        layout_load_images.setSizeConstraint(QLayout.SetFixedSize)
        layout_load_images.addWidget(self.button_browse_image_files, 0, 0)
        layout_load_images.addWidget(self.button_browse_image_folder, 0, 1)
        layout_load_images.addWidget(self.image_url_list, 1, 0, 1, 0)
        layout_load_images.addWidget(self.button_remove_selected_url, 2, 0)
        layout_load_images.addWidget(self.button_clear_url_list, 2, 1)
        for n in range(0, 1):
            layout_load_images.setRowStretch(n, 0)
            layout_load_images.setColumnStretch(n, 0)

        self.tab_widget.setTabText(0, "Load Images")
        self.tab_load_images.setLayout(layout_load_images)

    def init_tab_edit_images(self):
        """
        Initialize the grid layout for the Edit Image tab and add the widgets.  Then name the tab and
        add the grid to the tab.
        :return:
        """
        label_resolution = QLabel(text="Enter XY Resolution:")
        label_resolution.setToolTip("This is the resolution resize control.  Enter the new X and Y resolutions.")
        label_contrast = QLabel(text="Enter Contrast Value:")
        label_contrast.setToolTip("Inputting 1.3 means 30% more contrast.")
        label_rotate = QLabel(text="Enter Rotation Degrees:")
        label_rotate.setToolTip("Enter a custom rotation degree value or choose a specific rotation amount "
                                "from the combobox")
        label_sharpness = QLabel(text="Enter Sharpness Value:")
        label_sharpness.setToolTip("0 b/w, 1.0 orig, 1.0+ sharpen")
        label_brightness = QLabel(text="Enter Brightness Value:")
        label_brightness.setToolTip("0 b, 1.0 orig, 1.0+ brighten")
        label_apply_to_all_images = QLabel(text="Apply Edits to All Images?")

        layout_edit_images = QGridLayout()
        layout_edit_images.setSizeConstraint(QLayout.SetFixedSize)
        layout_edit_images.addWidget(self.combobox_active_image, 0, 0, 1, 3)
        layout_edit_images.addWidget(self.label_image_preview, 1, 0, 1, 3)
        layout_edit_images.addWidget(label_resolution, 2, 0)
        layout_edit_images.addWidget(label_contrast, 2, 2)
        layout_edit_images.addWidget(label_rotate, 4, 0)
        layout_edit_images.addWidget(label_sharpness, 4, 2)
        layout_edit_images.addWidget(label_brightness, 6, 2)
        layout_edit_images.addWidget(self.line_edit_x_res, 3, 0)
        layout_edit_images.addWidget(self.line_edit_y_res, 3, 1)
        layout_edit_images.addWidget(self.line_edit_contrast, 3, 2)
        layout_edit_images.addWidget(self.line_edit_sharpness, 5, 2)
        layout_edit_images.addWidget(self.line_edit_brightness, 7, 2)
        layout_edit_images.addWidget(self.line_edit_rotate, 5, 0)
        layout_edit_images.addWidget(self.combobox_rotation, 5, 1)
        layout_edit_images.addWidget(label_apply_to_all_images, 6, 0)
        layout_edit_images.addWidget(self.checkbox_apply_all_images, 6, 1)
        layout_edit_images.addWidget(self.button_toggle_preview, 7, 0)

        for n in range(0, 2):
            layout_edit_images.setRowStretch(n, 0)
            layout_edit_images.setColumnStretch(n, 0)

        self.tab_widget.setTabText(1, "Edit Images")
        self.tab_edit_images.setLayout(layout_edit_images)

    def init_tab_export_images(self):
        """
        Initialize the grid layout for the Export Image tab and add the widgets.  Then name the tab and
        add the grid to the tab.
        :return:
        """
        label_export_prefix_suffix = QLabel(text="Enter prefix/suffix for filename:")
        label_export_prefix_suffix.setToolTip("Add a prefix or suffix to the file name when saving out the file.")
        label_use_orig_filename = QLabel("Use Original Filename?")
        label_append_number = QLabel(text="Append Incremental Number?")

        layout_export_images = QGridLayout()
        layout_export_images.setSizeConstraint(QLayout.SetFixedSize)
        layout_export_images.addWidget(self.line_edit_export_dir, 0, 0, 1, 3)
        layout_export_images.addWidget(self.button_browse_export_dir, 0, 4)
        layout_export_images.addWidget(label_use_orig_filename, 1, 0)
        layout_export_images.addWidget(self.checkbox_use_orig_filename, 1, 1)
        layout_export_images.addWidget(self.line_edit_filename, 1, 2)
        layout_export_images.addWidget(self.line_edit_prefix, 2, 0)
        layout_export_images.addWidget(self.line_edit_suffix, 2, 1, 1, 2)
        layout_export_images.addWidget(label_append_number, 3, 0)
        layout_export_images.addWidget(self.checkbox_append_number, 3, 1)
        layout_export_images.addWidget(self.button_export_files, 4, 0)

        for n in range(0, 1):
            layout_export_images.setRowStretch(n, 0)
            layout_export_images.setColumnStretch(n, 0)

        self.tab_widget.setTabText(2, "Export Images")
        self.tab_export_images.setLayout(layout_export_images)

    def populate_image_list_widget(self):
        """
        Calls browse_for_files to let user open file dialog and select 1 or more files which is stored
        in selected_files
        :return:
        """
        self.load_images.browse_for_files()
        selected_files = self.load_images.selected_files
        self.image_url_list.addItems(selected_files)

    def clean_url_list(self):
        """
        Clear the file list widget
        :return:
        """
        self.image_url_list.clear()
