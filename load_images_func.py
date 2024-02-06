from PySide6.QtWidgets import QFileDialog

NAME_FILTERS = "Images (*.png *.jpg *.jpeg *.bmp *.gif)"


class LoadImages:
    """
    This class contains the function logic to the GUI widgets that pertain to the act of loading in
    the image files to be processed through editing and export.
    """
    def __init__(self):
        self.selected_files = []

    def browse_for_files(self):
        """
        Open the Qt file dialog to allow the user to select 1 or more files.  Ensure the files are of image
        format.
        :return:
        """
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)

        # Enforce the use of the Qt File Dialog
        file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)

        # Returns the absolute file path with a filter for image file types only
        self.selected_files, _ = file_dialog.getOpenFileNames(filter=NAME_FILTERS)

    def browse_for_folder(self):
        pass

    def clean_url_list(self):
        pass

    def remove_selected_urls(self):
        pass
