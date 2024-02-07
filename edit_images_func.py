import logging
import sys


class EditImages:
    """
    This class contains the function logic to the GUI widgets that pertain to the act of editing
    the image files.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logger()

    def setup_logger(self):
        log_format = logging.Formatter("%(asctime)s: %(module)s: %(levelname)s: %(message)s",
                                       datefmt="%Y-%m-%d %H:%M:%S")
        self.logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(log_format)
        self.logger.addHandler(stream_handler)
