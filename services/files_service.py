import os
import uuid
from utils import constants
from quart.datastructures import FileStorage


def remove_file(file_url: str = None, host_url: str = None, root_path: str = None):
    if file_url is None or host_url is None or root_path is None:
        raise ValueError("file_url, host_url, and root_path must be provided")
    images_folder = os.path.join(root_path, '../api', constants.IMAGES_REPOSITORY)
    file_name = file_url.split('/')[-1]
    file_to_remove_path = os.path.join(images_folder, file_name)
    if os.path.exists(file_to_remove_path):
        os.remove(file_to_remove_path)


async def save_file(file: FileStorage = None, host_url: str = None, root_path: str = None, repository: str = None):
    upload_folder = os.path.join(root_path, '../api', repository)
    os.makedirs(upload_folder, exist_ok=True)
    image_id = f"{str(uuid.uuid4())}_{file.filename}"
    file_path = os.path.join(upload_folder, image_id)
    await file.save(file_path)
    image_url = f"{host_url}api/images/{image_id}"
    return image_url, file_path

