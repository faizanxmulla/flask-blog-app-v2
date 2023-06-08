import os
from werkzeug.utils import secure_filename

from flask import current_app, flash

# --------------------------------------------------------------------------------

def save_profile(image_file):
    """
    Save the image file to the server and return the path
    """
    filename = secure_filename(image_file.filename)
    file_path = os.path.join(current_app.config['PROFILE_PICS_FOLDER'], filename)

    print(file_path)

    # with open(file_path, 'wb') as f:
    #     f.write(image_file.read())
    image_file.save(file_path)
    return file_path