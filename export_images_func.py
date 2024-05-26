from PySide6.QtWidgets import QFileDialog


class ExportImages:
    def __init__(self):
        self.file_dialog = QFileDialog()
        self.file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)

    def open_browse_directory_window(self):
        """
        Open the Qt file dialog to allow the user to select 1 or more files.  Ensure the files are of image
        format.
        :return:
        """
        self.file_dialog.setFileMode(QFileDialog.Directory)

        selected_directory = self.file_dialog.getExistingDirectory()

        return selected_directory
