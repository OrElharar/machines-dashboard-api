import os
from quart import Blueprint, send_file
from app.app import app
import utils.constants as constants

images_router = Blueprint('images', __name__)


@images_router.route('/<string:image_id>', methods=['GET'])
async def get_image(image_id):
    try:
        upload_folder = os.path.join(app.root_path, '../api/', constants.IMAGES_REPOSITORY)
        image_path = os.path.join(upload_folder, image_id)

        if not os.path.exists(image_path):
            return 'Image not found', 404

        return await send_file(image_path, mimetype='image/jpeg')

    except Exception as e:
        return str(e), 500
