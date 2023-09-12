import os
from quart import request, jsonify, Blueprint
from app.app import app
from quart_jwt_extended import jwt_required
from utils import constants
from services import validations_service
from services.files_service import remove_file, save_file


machines_images_router = Blueprint('machines_images', __name__)


@machines_images_router.route('/<int:id>/images', methods=['POST'])
@jwt_required
async def upload_image(id: int):
    file_key = constants.UPLOAD_IMAGE_KEY
    if file_key not in (await request.files):
        return jsonify({'error': 'No file part'}), 400

    file = (await request.files)[file_key]
    is_valid, error_message = validations_service.validate_image(file, app.config['MAX_CONTENT_UPLOADED_LENGTH'])
    if not is_valid:
        return jsonify({'error': error_message}), 400
    image_url, file_path = await save_file(file=file, host_url=request.host_url, root_path=app.root_path, repository=constants.IMAGES_REPOSITORY)
    try:
        await app.db.fetch_val(
            """SELECT insert_machine_image( :machine_id, :image_url );""",
            values={'machine_id': id, 'image_url': image_url},
        )
    except Exception as _e:
        os.remove(file_path)
        return jsonify({'message': "Failed to save image"}), 500
    return jsonify({'imageUrl': image_url}), 200


@machines_images_router.route('/<int:id>/images', methods=['DELETE'])
@jwt_required
async def delete_image(id: int):
    try:
        image_url = await app.db.fetch_val(
            """SELECT delete_machine_image_and_get_url( :machine_id );""",
            values={'machine_id': id},
        )
    except Exception as _e:
        return jsonify({'message': "Failed to delete image"}), 500
    if image_url is None:
        return jsonify({'message': "Image not found"}), 404
    remove_file(file_url=image_url, host_url=request.host_url, root_path=app.root_path)
    return jsonify({'message': "Image deleted"}), 200