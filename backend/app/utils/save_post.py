import os
from flask import current_app
from werkzeug.utils import secure_filename
# --------------------------------------------------------------------------------

# handling POSTS

def save_post(image_file):
    """
    Save the image file to the server and return the path
    """
    filename = secure_filename(image_file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    print(file_path)

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    image_file.save(file_path)
    return file_path

