def is_file_extension_valid(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif', 'webp'}


def is_file_size_valid(file, max_size):
    return file.content_length <= max_size


def validate_image(file, max_size):
    is_valid = True
    error_message = None
    if not is_file_extension_valid(file.filename):
        is_valid = False
        error_message = 'Invalid file extension'
    if is_valid and not is_file_size_valid(file, max_size):
        is_valid = False
        error_message = 'Invalid file size'
    return is_valid, error_message


