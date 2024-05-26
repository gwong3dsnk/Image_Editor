from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout


class ExportDialogBox(QDialog):
    """
    Called when the user clicks on button to export images to files.  If there are any issues, this class will open
    a new popup window with messages to inform the user.
    """
    def __init__(self, messages):
        """
        Defines the attributes for the QDialog window.
        :param messages: Predetermined messages to handle the various issues for export.  Found in gui_main.py in the
        export_image_to_file func.
        """
        super().__init__()

        self.message_list = messages

        self.setWindowTitle("Warning! Missing Fields")
        self.setMinimumSize(500, 100)

        layout = QVBoxLayout()
        label_key_msg = QLabel("Cannot process export due to missing fields:")
        layout.addWidget(label_key_msg)

        self.label_message = QLabel(messages)
        layout.addWidget(self.label_message)

        btn_close_window = QPushButton("Close")
        btn_close_window.clicked.connect(self.reject)
        layout.addWidget(btn_close_window)

        self.setLayout(layout)
