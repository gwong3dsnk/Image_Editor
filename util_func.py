import os

TRUNCATE_MAX = 50
TRUNCATE_PREFIX_LENGTH = 20
TRUNCATE_SUFFIX_LENGTH = 40


def is_file_image(filepath):
    """
    Check to make sure the passed in filepath is in face an image file.
    :param filepath:
    :return:
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    _, ext = os.path.splitext(filepath)

    return True if ext.lower() in image_extensions else False


def truncate_file_path(img_path):
    """
    Truncate the file paths in the passed in list so they can be displayed and fitted into the Edit Image combobox
    widget.
    :param img_path:
    :return truncated_file_path:
    """
    if len(img_path) <= TRUNCATE_MAX:
        truncated_file_path = img_path
    else:
        truncated_path = f"{img_path[:TRUNCATE_PREFIX_LENGTH]}...{img_path[-TRUNCATE_SUFFIX_LENGTH:]}"
        truncated_file_path = truncated_path

    return truncated_file_path
