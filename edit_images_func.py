import logging
import sys
from image_job import ImageJob
from PySide6.QtGui import QTransform, QPixmap
from PySide6.QtCore import Qt
from PIL import Image, ImageEnhance, ImageQt


class EditImages:
    """
    This class contains the function logic to the GUI widgets that pertain to the act of editing
    the image files.
    """
    def __init__(self, label_preview_widget):
        self.logger = logging.getLogger(__name__)
        self.setup_logger()
        self.active_job_index = 0
        self.pixmap = QPixmap()
        self.img_job = ImageJob()
        self.label_preview_widget = label_preview_widget

    def setup_logger(self):
        log_format = logging.Formatter("%(asctime)s: %(module)s: %(levelname)s: %(message)s",
                                       datefmt="%Y-%m-%d %H:%M:%S")
        self.logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(log_format)
        self.logger.addHandler(stream_handler)

    def set_active_img_job(self, combobox_active_image, load_images_obj):
        """
        Based on user selection from Edit Panel combobox, get the appropriate image job from load_images obj
        and set it to the self.img_job attr.
        :param combobox_active_image: QComboBox from Edit Panel, user-selected
        :param load_images_obj: LoadImages() class object
        :return:
        """
        self.active_job_index = combobox_active_image.currentIndex() - 1
        self.img_job = load_images_obj.all_image_jobs[self.active_job_index]

    def create_pixmap_object(self, image_url_list):
        """
        Get the image path from the list widget in the load tab, create the pixmap, load pixmap into QLabel
        :param image_url_list: QListWidget containing full abs image file paths
        :return scaled_pixmap:
        """
        item = image_url_list.item(self.active_job_index)
        self.pixmap = QPixmap(item.text())

        scaled_pixmap = (self.pixmap.scaled(
            self.label_preview_widget.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation)
        )

        return scaled_pixmap

    def calc_img_wh(self, new_img_wh, is_refreshing_height):
        """
        Depending on if focus has left height or width QLineEdit, calculate the other value using img aspect ratio.
        :param new_img_wh: (int)
        :param is_refreshing_height: (bool)
        :return:
        """
        active_img_job_aspect_ratio = self.img_job.img_aspect_ratio

        if is_refreshing_height:
            if active_img_job_aspect_ratio > 1:
                new_img_height = int(round(new_img_wh / active_img_job_aspect_ratio, 0))
            else:
                new_img_height = int(round(new_img_wh * active_img_job_aspect_ratio, 0))

            # Store value into image job for export
            self.img_job.img_height = new_img_height
            return new_img_height
        else:
            if active_img_job_aspect_ratio > 1:
                new_img_width = int(round(new_img_wh * active_img_job_aspect_ratio, 0))
            else:
                new_img_width = int(round(new_img_wh / active_img_job_aspect_ratio, 0))

            # Store value into image job for export
            self.img_job.img_width = new_img_width
            return new_img_width

    def calc_img_rotation(self, rotation_value):
        """
        Take in args containing user input rotation degrees and widgets and returns a scaled/rotated pixmap
        :param rotation_value: (int) User entered rotation value
        :return scaled_pixmap: Pixmap that has been rotated
        """
        rotated_pixmap = self.pixmap.transformed(QTransform().rotate(rotation_value))
        scaled_pixmap = rotated_pixmap.scaled(
            self.label_preview_widget.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        # Store value into image job for export
        self.img_job.img_rotation = rotation_value
        return scaled_pixmap

    def calc_img_contrast(self, contrast_value, rotation_value):
        """
        Executes the contrast adjustment on the current pixmap image.
        :param contrast_value: (float)
        :param rotation_value: (int)
        :return:
        """
        image = self.convert_pixmap_to_pil()
        img_enhancer = ImageEnhance.Contrast(image)
        contrasted_img = img_enhancer.enhance(contrast_value)
        self.convert_pil_to_pixmap(contrasted_img)

        # Create the scaled pixmap and return (take into account previously set values)
        scaled_pixmap = self.calc_img_rotation(rotation_value)
        return scaled_pixmap

    def convert_pixmap_to_pil(self):
        """
        Converts from a pixmap image to a Pillow Image
        :return image: (Image)
        """
        pil_img = self.pixmap.toImage()
        image = Image.fromqimage(pil_img)
        return image

    def convert_pil_to_pixmap(self, pil_img):
        """
        Converts a given pillow Image to a Pixmap and updates the self.pixmap attr.
        :param pil_img: (Image)
        :return:
        """
        image_qt = ImageQt.ImageQt(pil_img)
        self.pixmap = QPixmap.fromImage(image_qt)
