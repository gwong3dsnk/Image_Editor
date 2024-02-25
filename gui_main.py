import sys
from PySide6.QtCore import Qt
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import *
from load_images_func import LoadImages
from edit_images_func import EditImages
import util_func


class GuiMain(QWidget):
    """
    The UI class.  Sets up the GUI for the Image Editing application.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo Editor")
        self.setMinimumSize(500, 350)

        self.pixmap = QtGui.QPixmap()
        self.img_job = []
        self.active_img_job_index = 0

        # Instantiate func classes to access data logic
        self.load_images = LoadImages()
        self.edit_images = EditImages()

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
        self.button_browse_image_files = QPushButton(text="Add Image File(s)")
        self.button_browse_image_files.clicked.connect(self.populate_list_with_files)
        self.button_browse_image_folder = QPushButton(text="Add Image Folder")
        self.button_browse_image_folder.clicked.connect(self.populate_list_with_dir_files)
        self.image_url_list = QListWidget()
        self.image_url_list.setFixedSize(500, 250)
        self.image_url_list.setSelectionMode(QListWidget.MultiSelection)
        self.button_clear_url_list = QPushButton(text="Clear File(s)")
        self.button_clear_url_list.clicked.connect(self.clean_url_list)
        self.button_remove_selected_url = QPushButton(text="Remove Selected File(s)")
        self.button_remove_selected_url.clicked.connect(self.remove_selected_urls)

        # Initialize image edit widgets
        self.label_image_preview = QLabel()
        self.label_image_preview.setFixedSize(500, 400)
        self.label_image_preview.setScaledContents(False)
        self.label_image_preview.setStyleSheet("background-color: black;")
        self.label_resolution = QLabel(text="Original Resolution:")
        self.label_resolution.setToolTip("This is the resolution resize control.  Enter the new X and Y resolutions.")
        self.line_edit_x_res = QLineEdit()
        self.line_edit_x_res.setPlaceholderText("New X Res")
        self.line_edit_x_res.editingFinished.connect(self.calc_img_height)
        self.line_edit_y_res = QLineEdit()
        self.line_edit_y_res.setPlaceholderText("New Y Res")
        self.line_edit_y_res.editingFinished.connect(self.calc_img_width)
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
        self.combobox_active_image.currentIndexChanged.connect(self.display_selected_image)
        self.button_toggle_preview = QPushButton(text="Toggle Image Changes")
        self.button_apply_to_preview = QPushButton(text="Apply to Preview")
        self.checkbox_apply_all_images = QCheckBox()
        self.checkbox_apply_all_images.setChecked(False)
        self.checkbox_keep_aspect_ratio = QCheckBox()
        self.checkbox_keep_aspect_ratio.setChecked(True)

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
        label_contrast = QLabel(text="Enter Contrast Value:")
        label_contrast.setToolTip("Inputting 1.3 means 30% more contrast.")
        label_keep_aspect_ratio = QLabel(text="Keep Aspect Ratio?")
        label_sharpness = QLabel(text="Enter Sharpness Value:")
        label_sharpness.setToolTip("0 b/w, 1.0 orig, 1.0+ sharpen")
        label_brightness = QLabel(text="Enter Brightness Value:")
        label_brightness.setToolTip("0 b, 1.0 orig, 1.0+ brighten")
        label_apply_to_all_images = QLabel(text="Apply Edits to All Images?")

        layout_edit_images = QGridLayout()
        layout_edit_images.setSizeConstraint(QLayout.SetFixedSize)
        layout_edit_images.addWidget(self.combobox_active_image, 0, 0, 1, 3)
        layout_edit_images.addWidget(self.label_image_preview, 1, 0, 1, 3)
        layout_edit_images.addWidget(self.label_resolution, 2, 0, 1, 1)
        layout_edit_images.addWidget(label_contrast, 2, 2)
        layout_edit_images.addWidget(label_keep_aspect_ratio, 4, 0)
        layout_edit_images.addWidget(self.checkbox_keep_aspect_ratio, 4, 1)
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
        layout_edit_images.addWidget(self.button_apply_to_preview, 7, 0)
        layout_edit_images.addWidget(self.button_toggle_preview, 7, 1)

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

    def populate_list_with_files(self):
        """
        Calls browse_for_files from LoadImages class to let user open file dialog and select 1 or more files
        which is stored in the selected_files_abs_paths attr.
        :return:
        """
        self.load_images.browse_for_files()
        selected_files = self.load_images.selected_files_abs_paths
        self.load_images.check_list_for_duplicates(self.image_url_list, selected_files)
        refined_file_list = self.load_images.refined_file_list

        # Add the img paths to the appropriate ui widgets
        if refined_file_list:
            self.add_img_path_to_widgets(refined_file_list)

        # Reset vars for next load pass and populate the active img combobox
        self.load_images.reset_init_vars()

    def populate_list_with_dir_files(self):
        """
        Calls browse_for_folder from LoadImages class to let user open file dialog and select a directory.  The files
        are parsed then stored in the dir_selected_files_abs_paths attr.
        :return:
        """
        # User selects folder and we process files to check for duplicates.  Refined_File_List contains the new unique
        # items to be added.
        self.load_images.browse_for_folder()
        dir_selected_files = self.load_images.dir_selected_files_abs_paths
        self.load_images.check_list_for_duplicates(self.image_url_list, dir_selected_files)
        refined_file_list = self.load_images.refined_file_list

        # Add the img paths to the appropriate ui widgets
        if refined_file_list:
            self.add_img_path_to_widgets(refined_file_list)

        # Reset vars for next load pass and populate the active img combobox
        self.load_images.reset_init_vars()

    def populate_active_image_combobox(self, img_path):
        """
        Passes the image path to func to truncate it and add the truncated version to the edit tab's combobox.
        :param img_path:
        :return:
        """
        truncated_file_paths = util_func.truncate_file_path(img_path)
        self.combobox_active_image.addItem(truncated_file_paths)

    def add_img_path_to_widgets(self, refined_file_list):
        """
        So long as we have new unique items to add, create a new image job object for each item and add the
        img_path attr to the list widget and the truncated path to the edit tab combobox.
        :param refined_file_list:
        :return:
        """
        self.load_images.create_image_jobs(refined_file_list)
        self.img_job = self.load_images.image_jobs
        for job in self.img_job:
            self.image_url_list.addItem(job.img_path)
            self.populate_active_image_combobox(job.img_path)

    def clean_url_list(self):
        """
        Clear the file list widget and also reset the active image combobox in the edit tab while keeping the first
        default item.
        :return:
        """
        self.image_url_list.clear()
        while self.combobox_active_image.count() > 1:
            self.combobox_active_image.removeItem(1)

    def remove_selected_urls(self):
        """
        Remove all selected items from the list widget
        :return:
        """
        selected_items = self.image_url_list.selectedItems()
        for item in selected_items:
            self.image_url_list.takeItem(self.image_url_list.row(item))

    def display_selected_image(self):
        """
        Triggers when the active image combobox detects a change.  Get the index-1 (to ignore the default combobox
        item), use that index to get the full untruncated absolute path from the list widget and load that image
        into the label.
        :return:
        """
        if self.combobox_active_image.currentIndex() != 0:
            self.active_img_job_index = self.combobox_active_image.currentIndex() - 1
            item = self.image_url_list.item(self.active_img_job_index)
            pil_img = self.edit_images.create_pil_obj(item.text())

            self.pixmap = QtGui.QPixmap.fromImage(pil_img)

            self.label_image_preview.setPixmap(self.pixmap.scaled(
                self.label_image_preview.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation)
            )

            # Get the original resolution and display it in the label
            self.label_resolution.setText(f"Original Resolution: {self.pixmap.width()} x {self.pixmap.height()}")
            self.line_edit_x_res.setText(str(self.pixmap.width()))
            self.line_edit_y_res.setText(str(self.pixmap.height()))
        else:
            self.label_image_preview.clear()

    def calc_img_height(self):
        """
        Everytime a user enters data into the x LineEdit and focus leaves the LineEdit, this function is called
        to calculate the height based on aspect ratio checkbox state.
        :return:
        """
        if self.label_image_preview.pixmap() is not None:
            new_img_width = int(self.line_edit_x_res.text())

            if self.checkbox_keep_aspect_ratio.isChecked():
                active_img_job_aspect_ratio = self.img_job[self.active_img_job_index].img_aspect_ratio
                if active_img_job_aspect_ratio > 1:
                    new_img_height = int(round(new_img_width / active_img_job_aspect_ratio, 0))
                else:
                    new_img_height = int(round(new_img_width * active_img_job_aspect_ratio, 0))

                self.line_edit_y_res.setText(str(new_img_height))

    def calc_img_width(self):
        """
        Everytime a user enters data into the y LineEdit and focus leaves the LineEdit, this function is called
        to calculate the height based on aspect ratio checkbox state.
        :return:
        """
        if self.label_image_preview.pixmap() is not None:
            new_img_height = int(self.line_edit_y_res.text())

            if self.checkbox_keep_aspect_ratio.isChecked():
                active_img_job_aspect_ratio = self.img_job[self.active_img_job_index].img_aspect_ratio
                if active_img_job_aspect_ratio > 1:
                    new_img_width = int(round(new_img_height * active_img_job_aspect_ratio, 0))
                else:
                    new_img_width = int(round(new_img_height / active_img_job_aspect_ratio, 0))
                self.line_edit_x_res.setText(str(new_img_width))
