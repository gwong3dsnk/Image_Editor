import os
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

    def get_filename_with_inserts(self, base_filename, prefix, suffix):
        """
        If user has declared to use a prefix and/or suffix, detect the entered values and create the new name string
        :param base_filename:
        :param prefix:
        :param suffix:
        :return:
        """
        if prefix != "" and suffix == "":
            filename_with_inserts = f"{prefix}_{base_filename}"
        elif prefix != "" and suffix != "":
            filename_with_inserts = f"{prefix}_{base_filename}_{suffix}"
        elif prefix == "" and suffix != "":
            filename_with_inserts = f"{base_filename}_{suffix}"
        else:
            filename_with_inserts = f"{base_filename}"

        return filename_with_inserts

    def get_filename_with_increm_num(self, export_dir, filename_with_inserts, chosen_file_format, filename_with_format):
        """
        Adds incremental number to end of filename.
        :param export_dir:
        :param filename_with_inserts:
        :param chosen_file_format:
        :param filename_with_format:
        :return:
        """
        dir_files = os.listdir(export_dir)
        increm_num_list = []
        for file in dir_files:
            file_path = os.path.join(export_dir, file)
            if os.path.isfile(file_path):
                if filename_with_inserts in file:
                    extracted_increm_num = file.split(".")[0].split("_")[-1]
                    if extracted_increm_num.isdigit():
                        increm_num_list.append(int(extracted_increm_num))

        if increm_num_list:
            increm_num_list.sort()
            for num in range(len(increm_num_list) - 1):
                if increm_num_list[num + 1] - increm_num_list[num] != 1:
                    increm_num = "{:02d}".format(increm_num_list[num] + 1)
                    filename_with_format = f"{filename_with_inserts}_{increm_num}.{chosen_file_format}"
                    break

            if filename_with_format == "" and increm_num_list[-1] + 1 not in increm_num_list:
                increm_num = "{:02d}".format(increm_num_list[-1] + 1)
                filename_with_format = f"{filename_with_inserts}_{increm_num}.{chosen_file_format}"
        else:
            filename_with_format = f"{filename_with_inserts}_01.{chosen_file_format}"

        return filename_with_format

    def save_image_out(self, pil_img, export_dir, filename_with_format):
        export_path = os.path.join(export_dir, filename_with_format)
        pil_img.save(export_path)
