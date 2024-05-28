import sys, os
from PySide6.QtCore import Qt
from PySide6 import QtGui
from PySide6.QtWidgets import *
from load_images_func import LoadImages
from edit_images_func import EditImages
from export_images_func import ExportImages
from export_dialog_box import ExportDialogBox
import util_func


class GuiMain(QWidget):
    """
    The UI class.  Sets up the GUI for the Image Editing application.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo Editor")
        self.setMinimumSize(500, 350)

        self.img_job = None
        self.is_attr_modified = False
        self.img_attributes = []
        self.is_previewing_default = False

        # Create the top menu bar
        self.menu_bar = QMenuBar(self)
        self.create_menu_bar()

        # Create the window tab objects
        self.tab_load_images = QWidget(self)
        self.tab_edit_images = QWidget(self)
        self.tab_export_images = QWidget(self)
        self.tab_widget = QTabWidget(self)
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
        self.label_image_preview.setAlignment(Qt.AlignCenter)
        self.label_image_preview.setStyleSheet("background-color: black;")
        self.label_resolution = QLabel(text="Original Resolution:")
        self.label_resolution.setToolTip("This is the resolution resize control.  Enter the new X and Y resolutions.")
        self.label_keep_aspect_ratio = QLabel(text="Keep Aspect Ratio (0.00)?")
        self.label_displayed_image = QLabel(text="Displayed: N/A")
        self.line_edit_x_res = QLineEdit()
        self.line_edit_x_res.setPlaceholderText("New X Res")
        self.line_edit_x_res.editingFinished.connect(self.refresh_img_height)
        self.line_edit_y_res = QLineEdit()
        self.line_edit_y_res.setPlaceholderText("New Y Res")
        self.line_edit_y_res.editingFinished.connect(self.refresh_img_width)
        self.spinbox_contrast = QDoubleSpinBox()
        self.spinbox_contrast.setValue(1)
        self.spinbox_contrast.setRange(0.01, 10)
        self.spinbox_contrast.setDecimals(2)
        self.spinbox_contrast.setSingleStep(0.1)
        self.spinbox_contrast.setToolTip("i.e. Enter 1.3 for 30%")
        self.spinbox_contrast.editingFinished.connect(self.refresh_pixmap_img)
        self.spinbox_rotate = QSpinBox()
        self.spinbox_rotate.setValue(0)
        self.spinbox_rotate.setRange(-360, 360)
        self.spinbox_rotate.setSingleStep(5)
        self.spinbox_rotate.editingFinished.connect(self.refresh_pixmap_img)
        self.spinbox_sharpness = QDoubleSpinBox()
        self.spinbox_sharpness.setValue(1)
        self.spinbox_sharpness.setMinimum(0.01)
        self.spinbox_sharpness.setSingleStep(0.01)
        self.spinbox_sharpness.setToolTip("Enter value.  i.e. 0 b/w, 1.0 orig, 1.0+ sharpen")
        self.spinbox_sharpness.editingFinished.connect(self.refresh_pixmap_img)
        self.spinbox_brightness = QDoubleSpinBox()
        self.spinbox_brightness.setValue(1)
        self.spinbox_brightness.setMinimum(0.01)
        self.spinbox_brightness.setSingleStep(0.01)
        self.spinbox_brightness.setToolTip("Enter value.  i.e. 0 b, 1.0 orig, 1.0+ brighten")
        self.spinbox_brightness.editingFinished.connect(self.refresh_pixmap_img)
        self.combobox_active_image = QComboBox()
        self.combobox_active_image.addItem("Select an Image to Edit")
        self.combobox_active_image.currentIndexChanged.connect(self.display_selected_image)
        self.button_toggle_preview = QPushButton(text="Toggle Image Preview")
        self.button_toggle_preview.setEnabled(False)
        self.button_toggle_preview.clicked.connect(self.toggle_image_preview)
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
        self.button_browse_export_dir.clicked.connect(self.browse_to_export_directory)
        self.button_export_files = QPushButton(text="Export File(s)")
        self.button_export_files.clicked.connect(self.export_image_to_file)
        self.combobox_image_format = QComboBox()
        self.combobox_image_format.addItem("PNG")
        self.combobox_image_format.addItem("JPEG")
        self.combobox_image_format.addItem("BMP")
        self.combobox_image_format.addItem("GIF")
        self.combobox_export_all_or_one = QComboBox()
        self.combobox_export_all_or_one.addItem("Export Current Active Image")
        self.combobox_export_all_or_one.addItem("Export All Images")
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
        self.checkbox_use_orig_filename.clicked.connect(self.toggle_user_filename)
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

        # Instantiate func classes to access data logic
        self.load_images = LoadImages()
        self.edit_images = EditImages(self.label_image_preview)
        self.export_images = ExportImages()

    def create_menu_bar(self):
        """
        Create the menu bar and subsequent menu items
        :return:
        """
        # Create the menu
        file_menu = QMenu("File", self)
        edit_menu = QMenu("Edit", self)

        # Create the menu actions
        exit_action = QtGui.QAction("Exit", self)
        reset_current_image = QtGui.QAction("Reset Current Image", self)
        reset_all_images = QtGui.QAction("Reset All Images", self)

        # Create the function call when the action is triggered.
        exit_action.triggered.connect(self.exit_action_triggered)

        # Add the action to the menu
        file_menu.addAction(exit_action)
        edit_menu.addAction(reset_current_image)
        edit_menu.addAction(reset_all_images)

        # Add the menu to the parent QMenuBar
        self.menu_bar.addMenu(file_menu)
        self.menu_bar.addMenu(edit_menu)

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
        label_contrast = QLabel(text="Contrast:")
        label_contrast.setToolTip("Inputting 1.3 means 30% more contrast.")
        label_sharpness = QLabel(text="Sharpness:")
        label_sharpness.setToolTip("0 b/w, 1.0 orig, 1.0+ sharpen")
        label_brightness = QLabel(text="Brightness:")
        label_brightness.setToolTip("0 b, 1.0 orig, 1.0+ brighten")
        label_apply_to_all_images = QLabel(text="Apply Edits to All Images?")
        label_rotation = QLabel(text="Rotation:")
        label_rotation.setToolTip("Enter rotation value in degrees (i.e. 90 for 90 degrees)")

        layout_edit_images = QGridLayout()
        layout_edit_images.setSizeConstraint(QLayout.SetFixedSize)
        layout_edit_images.addWidget(self.combobox_active_image, 0, 0, 1, 3)
        layout_edit_images.addWidget(self.label_image_preview, 1, 0, 1, 3)
        layout_edit_images.addWidget(self.label_resolution, 2, 0, 1, 1)
        layout_edit_images.addWidget(label_contrast, 2, 2)
        layout_edit_images.addWidget(self.label_keep_aspect_ratio, 4, 0)
        layout_edit_images.addWidget(self.checkbox_keep_aspect_ratio, 4, 1)
        layout_edit_images.addWidget(label_sharpness, 4, 2)
        layout_edit_images.addWidget(label_brightness, 6, 2)
        layout_edit_images.addWidget(self.line_edit_x_res, 3, 0)
        layout_edit_images.addWidget(self.line_edit_y_res, 3, 1)
        layout_edit_images.addWidget(self.spinbox_contrast, 3, 2)
        layout_edit_images.addWidget(self.spinbox_sharpness, 5, 2)
        layout_edit_images.addWidget(self.spinbox_brightness, 7, 2)
        layout_edit_images.addWidget(label_rotation, 5, 0)
        layout_edit_images.addWidget(self.spinbox_rotate, 5, 1)
        layout_edit_images.addWidget(label_apply_to_all_images, 6, 0)
        layout_edit_images.addWidget(self.checkbox_apply_all_images, 6, 1)
        layout_edit_images.addWidget(self.button_toggle_preview, 7, 0)
        layout_edit_images.addWidget(self.label_displayed_image, 7, 1)

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
        label_use_orig_filename = QLabel(text="Use Original Filename?")
        label_append_number = QLabel(text="Append Incremental Number?")
        label_export_file_format = QLabel("File Format:")
        label_export_method = QLabel("Export Method:")

        layout_export_images = QGridLayout()
        layout_export_images.setSizeConstraint(QLayout.SetFixedSize)
        layout_export_images.addWidget(self.line_edit_export_dir, 0, 0, 1, 2)
        layout_export_images.addWidget(self.button_browse_export_dir, 0, 2)
        layout_export_images.addWidget(label_export_file_format, 1, 0)
        layout_export_images.addWidget(self.combobox_image_format, 1, 1)
        layout_export_images.addWidget(label_export_method, 2, 0)
        layout_export_images.addWidget(self.combobox_export_all_or_one, 2, 1)
        layout_export_images.addWidget(label_use_orig_filename, 3, 0)
        layout_export_images.addWidget(self.checkbox_use_orig_filename, 3, 1)
        layout_export_images.addWidget(self.line_edit_filename, 3, 2)
        layout_export_images.addWidget(self.line_edit_prefix, 4, 0)
        layout_export_images.addWidget(self.line_edit_suffix, 4, 1, 1, 1)
        layout_export_images.addWidget(label_append_number, 5, 0)
        layout_export_images.addWidget(self.checkbox_append_number, 5, 1)
        layout_export_images.addWidget(self.button_export_files, 6, 0)

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
        self.load_images.reset_load_attributes()

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
        self.load_images.reset_load_attributes()

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
        for job in self.load_images.all_image_jobs:
            self.image_url_list.addItem(job.img_path)
            self.populate_active_image_combobox(job.img_path)

    def clean_url_list(self):
        """
        Clear the file list widget and also reset the active image combobox in the edit tab while keeping the first
        default item.
        :return:
        """
        self.image_url_list.clear()
        self.load_images.reset_load_attributes()
        self.edit_images.reset_edit_attributes()
        self.load_images.all_image_jobs = []
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
            display_pixmap = self.get_img_job_pixmap()
            self.set_resolution_values()
            self.set_edit_control_values()
            self.label_image_preview.setPixmap(display_pixmap)
            self.is_attr_modified = False
        else:
            self.reset_edit_controls()
            self.label_image_preview.clear()

    def get_img_job_pixmap(self):
        self.edit_images.set_active_img_job(self.combobox_active_image, self.load_images)
        self.img_job = self.edit_images.img_job

        if self.img_job.img_enhanced_pixmap is None:
            self.is_previewing_default = True
            self.button_toggle_preview.setEnabled(False)
            if self.img_job.img_pixmap is None:
                display_pixmap = self.edit_images.create_default_pixmap_object(self.image_url_list)
                self.img_job.img_pixmap = display_pixmap
            else:
                display_pixmap = self.img_job.img_pixmap
        else:
            self.is_previewing_default = False
            self.button_toggle_preview.setEnabled(True)
            display_pixmap = self.img_job.img_enhanced_pixmap

        return display_pixmap

    def reset_edit_controls(self):
        self.is_attr_modified = True
        self.spinbox_rotate.setValue(0)
        self.spinbox_contrast.setValue(1)
        self.spinbox_sharpness.setValue(1)
        self.spinbox_brightness.setValue(1)
        self.line_edit_x_res.setText("")
        self.line_edit_y_res.setText("")
        self.label_displayed_image.setText("Displayed: N/A")
        self.label_resolution.setText("Original Resolution:")
        self.label_keep_aspect_ratio.setText("Keep Aspect Ratio (0.00)?")
        self.button_toggle_preview.setEnabled(False)

    def set_resolution_values(self):
        """
        Get the original resolution from img job object and display it in QLabel and QLineEdits
        :return:
        """
        orig_width = self.img_job.img_orig_width
        orig_height = self.img_job.img_orig_height

        self.label_resolution.setText(f"Original Resolution: {orig_width} x {orig_height}")

        self.line_edit_y_res.setText(orig_height) if self.img_job.img_new_height == "" else (
            self.line_edit_y_res.setText(self.img_job.img_new_height))

        self.line_edit_x_res.setText(orig_width) if self.img_job.img_new_width == "" else (
            self.line_edit_x_res.setText(self.img_job.img_new_width))

        self.spinbox_rotate.setValue(self.img_job.img_rotation)

    def set_edit_control_values(self):
        """
        Executed after user selects an img from the combobox.  If the image has custom attributes, set them into the
        UI widgets.
        :return:
        """
        # Update aspect ratio label with the active img aspect ratio.
        aspect_ratio_rounded = format(self.img_job.img_aspect_ratio, ".2f")
        self.label_keep_aspect_ratio.setText(f"Keep Aspect Ratio ({aspect_ratio_rounded})?")

        if self.img_job.img_rotation != 0 and self.spinbox_rotate.value() == 0:
            self.spinbox_rotate.setValue(self.img_job.img_rotation)

        self.spinbox_contrast.setValue(self.img_job.img_contrast)
        self.spinbox_brightness.setValue(self.img_job.img_brightness)
        self.spinbox_sharpness.setValue(self.img_job.img_sharpness)

    def refresh_img_height(self):
        """
        Everytime a user enters data into the x LineEdit and focus leaves the LineEdit, this function is called
        to calculate the height based on aspect ratio checkbox state.
        :return:
        """
        if self.label_image_preview.pixmap() is not None and self.checkbox_keep_aspect_ratio.isChecked():
            new_img_width = int(self.line_edit_x_res.text())
            new_img_height = self.edit_images.calc_img_wh(new_img_width, True)
            self.line_edit_y_res.setText(str(new_img_height))

    def refresh_img_width(self):
        """
        Called if user changes value in the y LineEdit AND focus leaves the LineEdit.  Calculates the width
        based on aspect ratio checkbox state.
        :return:
        """
        if self.label_image_preview.pixmap() is not None and self.checkbox_keep_aspect_ratio.isChecked():
            new_img_height = int(self.line_edit_y_res.text())
            new_img_width = self.edit_images.calc_img_wh(new_img_height, False)
            self.line_edit_x_res.setText(str(new_img_width))

    def refresh_pixmap_img(self):
        self.button_toggle_preview.setEnabled(True)
        if self.label_image_preview is not None:
            contrast_value = self.spinbox_contrast.value()
            rotation_value = self.spinbox_rotate.value()
            sharpness_value = self.spinbox_sharpness.value()
            brightness_value = self.spinbox_brightness.value()

            is_exporting_image = False
            pil_img = self.edit_images.convert_pixmap_to_pil(is_exporting_image)

            enhanced_pixmap = self.edit_images.calc_img_enhance(rotation_value, contrast_value,
                                                                sharpness_value, brightness_value, pil_img)
            self.edit_images.set_img_job_attr(rotation_value, contrast_value, sharpness_value, brightness_value)
            self.label_image_preview.setPixmap(enhanced_pixmap)

    def toggle_image_preview(self):
        """
        Called when user clicks on the Toggle Image Preview button.  Swaps between the default pixmap and the
        enhanced pixmap (if exists), ensuring that both adopt the proper rotation value.
        :return:
        """
        if self.label_image_preview is not None:
            if self.is_previewing_default:
                self.label_image_preview.setPixmap(self.img_job.img_enhanced_pixmap)
                self.label_displayed_image.setText("Displayed: Edited")
            else:
                self.label_image_preview.setPixmap(self.img_job.img_pixmap)
                self.label_displayed_image.setText("Displayed: Original")

    def browse_to_export_directory(self):
        """
        Executed when user clicks on the button to browse to a specific export directory
        :return:
        """
        selected_directory = self.export_images.open_browse_directory_window()
        self.line_edit_export_dir.setText(selected_directory)

    def toggle_user_filename(self):
        """
        Executed when the user checks or unchecks the checkbox on whether they wish to specify a unique file name or
        use the image's original filename.  Will toggle ReadOnly state on the line_edit widget.
        :return:
        """
        if self.line_edit_filename.isReadOnly():
            self.line_edit_filename.setStyleSheet("background-color: white;")
            self.line_edit_filename.setReadOnly(False)
        else:
            self.line_edit_filename.setStyleSheet("background-color: lightgray;")
            self.line_edit_filename.setReadOnly(True)

    def export_image_to_file(self):
        """
        Executed when the user clicks on the button to process export on the images.
        :return:
        """
        # self.export_error_checks()

        if self.combobox_active_image.currentIndex() == 0:
            self.open_dialog_box("Please choose an edited image from the Edit tab dropdown menu to export")

        if self.combobox_export_all_or_one.currentIndex() == 0:
            if self.img_job is not None:
                if self.img_job.img_enhanced_pixmap is not None:
                    is_exporting_image = True
                    chosen_file_format = self.combobox_image_format.currentText().lower()

                    if not self.checkbox_use_orig_filename.isChecked():
                        base_filename = self.line_edit_filename.text()
                    else:
                        base_filename = self.img_job.img_name

                    prefix = self.line_edit_prefix.text() if self.line_edit_prefix.text() != "" else ""
                    suffix = self.line_edit_suffix.text() if self.line_edit_suffix.text() != "" else ""

                    if prefix != "" and suffix == "":
                        filename_with_inserts = f"{prefix}_{base_filename}.{chosen_file_format}"
                    elif prefix != "" and suffix != "":
                        filename_with_inserts = f"{prefix}_{base_filename}_{suffix}.{chosen_file_format}"
                    elif prefix == "" and suffix != "":
                        filename_with_inserts = f"{base_filename}_{suffix}.{chosen_file_format}"
                    else:
                        filename_with_inserts = f"{base_filename}.{chosen_file_format}"

                    pil_img = self.edit_images.convert_pixmap_to_pil(is_exporting_image)
                    export_path = os.path.join(self.line_edit_export_dir.text(), filename_with_inserts)
                    pil_img.save(export_path)
                else:
                    self.open_dialog_box("The current image has no edits.  Please edit it first.")
            else:
                self.open_dialog_box("No images have been edited yet.")
        else:
            print("User has selected to export all images.")

    def export_error_checks(self):
        # Start by doing some error checks to make sure all the settings are set properly for export.
        if len(self.load_images.all_image_jobs) == 0:
            self.open_dialog_box("No edited images found.  Return to the load tab and load in some images to edit.  "
                                 "Make sure the images have been edited in the Edit tab.")
        else:
            message_list = ""
            if self.line_edit_export_dir.text() == "":
                message_list = f"No export directory chosen.  Please set one.\n"
            if not self.checkbox_use_orig_filename.isChecked() and self.line_edit_filename == "":
                message_list = (f"{message_list}You checked the box to use a new unique filename but "
                                f"haven't entered one.\n")
            self.open_dialog_box(message_list)

    def open_dialog_box(self, message_list):
        message_dialog_box = ExportDialogBox(message_list)
        message_dialog_box.exec_()
