class ImageJob:
    def __init__(self):
        # Initial image attributes
        self.img_path = ""
        self.img_name = ""
        self.img_orig_height = ""
        self.img_orig_width = ""
        self.img_aspect_ratio = 0
        self.img_format = ""
        self.img_pixmap = None

        # Modifiable attributes
        self.img_new_height = ""
        self.img_new_width = ""
        self.img_rotation = 0
        self.img_contrast = 1
        self.img_sharpness = 1
        self.img_brightness = 1
