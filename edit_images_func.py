import logging
import math
import sys
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
        self.img_job = None
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

    def create_default_pixmap_object(self, image_url_list):
        """
        Get the image path from the list widget in the load tab, create the pixmap, save it in the img_job
        default_pixmap attr, scale it to fit to QLabel.
        :param image_url_list: QListWidget containing full abs image file paths
        :return scaled_pixmap:
        """
        item = image_url_list.item(self.active_job_index)
        self.img_job.img_pixmap = QPixmap(item.text())
        self.img_job.img_enhanced_pixmap = self.img_job.img_pixmap

        scaled_default_pixmap = self.scale_pixmap(self.img_job.img_pixmap)

        return scaled_default_pixmap

    def calc_img_wh(self, new_img_res_val, is_calculating_height):
        """
        Executed when focus leaves height or width QLineEdit.  Receives either width or height value then calculates
        the other value using img aspect ratio.
        :param new_img_res_val: (int) Can be either a width or height value.
        :param is_calculating_height: (bool) True if new width has been passed in.  False if new height is passed in.
        :return:
        """
        if is_calculating_height:
            new_img_height = int(round(new_img_res_val * self.img_job.img_aspect_ratio, 0))

            # Store value into image job for export
            self.img_job.img_new_height = str(new_img_height)
            return new_img_height
        else:
            new_img_width = math.ceil(new_img_res_val * self.img_job.img_aspect_ratio_inv)

            # Store value into image job for export
            self.img_job.img_new_width = str(new_img_width)
            return new_img_width

    def calc_img_rotation(self, rotation_value, is_attr_modified):
        """
        Rotates the pixmap, rescales it and returns it.  Pixmap state is
        :param rotation_value: (int) User entered rotation value
        :param is_attr_modified: (bool) Flag if pixmap attr has been modified or not
        :return scaled_pixmap: Pixmap that has been rotated
        """
        rotated_pixmap = self.img_job.img_enhanced_pixmap.transformed(QTransform().rotate(rotation_value))
        scaled_pixmap = self.scale_pixmap(rotated_pixmap)
        self.img_job.img_enhanced_pixmap = scaled_pixmap

        if not is_attr_modified:
            self.img_job.img_rotation = rotation_value

        return scaled_pixmap

    def calc_img_enhance(self, *args):
        """
        Executes image enhancements based on user data entered
        :param args: [rotation_value, contrast_value, sharpness_value, brightness_value, pil_img]
        :return:
        """
        # image = self.convert_pixmap_to_pil()

        enhanced_img_contrast = ImageEnhance.Contrast(args[4]).enhance(args[1])
        enhanced_img_sharpness = ImageEnhance.Sharpness(enhanced_img_contrast).enhance(args[2])
        enhanced_img_brightness = ImageEnhance.Brightness(enhanced_img_sharpness).enhance(args[3])

        self.convert_pil_to_pixmap(enhanced_img_brightness)

        rotated_pixmap = self.calc_img_rotation(args[0], False)

        return rotated_pixmap

    def convert_pixmap_to_pil(self, is_exporting_image):
        """
        Converts from a pixmap image to a Pillow Image
        :return image: (Image)
        """
        if is_exporting_image:
            pil_img = self.img_job.img_enhanced_pixmap.toImage()
            image = Image.fromqimage(pil_img)
        else:
            pil_img = self.img_job.img_pixmap.toImage()
            image = Image.fromqimage(pil_img)
        return image

    def convert_pil_to_pixmap(self, pil_img):
        """
        Converts a given pillow Image to a Pixmap and updates the self.img_job.img_enhanced_pixmap attr.
        :param pil_img: (Image)
        :return:
        """
        image_qt = ImageQt.ImageQt(pil_img)
        self.img_job.img_enhanced_pixmap = QPixmap.fromImage(image_qt)

    def scale_pixmap(self, pixmap):
        """
        Take in a pixmap and scale it to fit properly into the QLabel for visual display to the user.
        :param pixmap:
        :return:
        """
        scaled_pixmap = pixmap.scaled(
            self.label_preview_widget.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        return scaled_pixmap

    def reset_edit_attributes(self):
        self.active_job_index = 0
        self.img_job = None

    def set_img_job_attr(self, *args):
        """
        Save user entered values for image properties to the img_job attributes.
        :param args:
        :return:
        """
        self.img_job.img_rotation = args[0]
        self.img_job.img_contrast = args[1]
        self.img_job.img_sharpness = args[2]
        self.img_job.img_brightness = args[3]
