# Image Editor (WIP)
After a vacation I would have way too many photos and I would want to downsize them to throw into my Google Photo albums and not exhaust my limited storage space.  
Photoshop actions is a good way to do it and how I've been doing it.  
But I decided to make this tool to also act as a refresh of Python for myself and get more practice into PySide6, threading, logging and pillow.

# NOTE THIS!
This tool is currently a WIP.  It is not complete yet.

# USE
You will start in the "Load Images" tab
1. Click on "Add Image File(s) to select 1+ files to add or "Add Image Folder" to add all image files with acceptable image formats.  Files will have their absolute path added to the list widget
2. Click on the "Edit Images" tab
3. Click on the dropdown at the top to select one of the images you added previously.  It will convert the image to a QPixmap, scale it and set it to the QLabel
4. Use the tools at the bottom to define new image resolution.  You won't see any change in the QPixmap.  The new resolution is read and used for export later.  While "Keep Aspect Ratio" is checked, changing either the X or Y resolution will auto-calculate the other value.
5. Changing rotation, contrast, sharpness, or brightness will result in immediate feedback in the QLabel as the QPixmap gets updated.
6. Click on "Toggle Image Preview" to swap between the original/default image and the modified version
7. TODO: Export Instructions 
