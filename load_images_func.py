from PySide6.QtWidgets import QFileDialog
import os
from PIL import Image
import image_job
import util_func
import logging
import sys

NAME_FILTERS = "Images (*.png *.jpg *.jpeg *.bmp *.gif)"


class LoadImages:
    """
    This class contains the function logic to the GUI widgets that pertain to the act of loading in
    the image files to be processed through editing and export.
    """
    def __init__(self):
        self.selected_files_abs_paths = []
        self.dir_selected_files_abs_paths = []
        self.refined_file_list = []
        self.all_image_jobs = []

        self.logger = logging.getLogger(__name__)
        self.setup_logger()

        self.file_dialog = QFileDialog()
        self.file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)

    def setup_logger(self):
        log_format = logging.Formatter("%(asctime)s: %(module)s: %(levelname)s: %(message)s",
                                       datefmt="%Y-%m-%d %H:%M:%S")
        self.logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(log_format)
        self.logger.addHandler(stream_handler)

    def browse_for_files(self):
        """
        Open the Qt file dialog to allow the user to select 1 or more files.  Ensure the files are of image
        format.
        :return:
        """
        self.file_dialog.setFileMode(QFileDialog.ExistingFiles)

        # Returns the absolute file path with a filter for image file types only
        files_paths, _ = self.file_dialog.getOpenFileNames(filter=NAME_FILTERS)

        self.selected_files_abs_paths = [path for path in files_paths]

    def browse_for_folder(self):
        """
        Open the Qt file dialog to allow the user to select a folder and load all the files found within.
        Ensure the files are of image format.
        :return:
        """
        self.file_dialog.setFileMode(QFileDialog.Directory)

        # Returns the absolute file path with a filter for image file types only
        selected_dir = self.file_dialog.getExistingDirectory()

        if selected_dir:
            get_existing_files = os.listdir(selected_dir)
            for file in get_existing_files:
                file_abs_path = os.path.join(selected_dir, file)
                if os.path.isfile(file_abs_path):
                    if util_func.is_file_image(file_abs_path):
                        norm_path = file_abs_path.replace("\\", "/")
                        self.dir_selected_files_abs_paths.append(norm_path)
                    else:
                        self.logger.warning(f"This file [{file}] is not an image.  Skipping.")

    def check_list_for_duplicates(self, list_widget, file_list):
        """
        Checks for duplicates that already exist in the list widget.  If no dups exist, add to the refined list and
        return it.
        :param list_widget: image_url_list in GuiMain()
        :param file_list: list of absolute path of file images
        """
        list_widget_item_num = list_widget.count()
        list_item_text = []

        if list_widget_item_num:
            for n in range(list_widget_item_num):
                item = list_widget.item(n)
                list_item_text.append(item.text())

            for path in file_list:
                if path in list_item_text:
                    break
                else:
                    self.refined_file_list.append(path)
        else:
            self.refined_file_list = file_list

    def reset_load_attributes(self):
        self.selected_files_abs_paths = []
        self.dir_selected_files_abs_paths = []
        self.refined_file_list = []

    def create_image_jobs(self, refined_file_list):
        """
        For each file selected to load in, create an img_job object and setup default attribute values.
        :param refined_file_list:
        :return:
        """
        for file in refined_file_list:
            img_job_obj = image_job.ImageJob()
            with Image.open(file) as ip:
                img_job_obj.img_orig_height = img_job_obj.img_new_height = str(ip.height)
                img_job_obj.img_orig_width = img_job_obj.img_new_width = str(ip.width)
                img_job_obj.img_aspect_ratio = ip.height / ip.width
                img_job_obj.img_aspect_ratio_inv = ip.width / ip.height
                img_job_obj.img_format = ip.format
                img_job_obj.img_path = file
                img_job_obj.img_name = file.rpartition("/")[2].split(".")[0]

            self.all_image_jobs.append(img_job_obj)
