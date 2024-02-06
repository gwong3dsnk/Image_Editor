import sys
from PySide6.QtWidgets import QApplication
from gui_main import GuiMain


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui_instance = GuiMain()
    gui_instance.show()
    sys.exit(app.exec())
