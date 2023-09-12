import re
from quart import jsonify, Blueprint
from app.app import app

from quart_jwt_extended import jwt_required
from entities.manufacturer import Manufacturer
from utils import logger

manufacturers_router = Blueprint('manufacturers', __name__)


def snake_to_camel(s):
    return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), s)


@manufacturers_router.route('/', methods=['GET'])
@jwt_required
async def get_all_manufacturers():
    """Get all manufacturers."""
    try:
        result = await app.db.fetch_all(
            """SELECT * from select_all_manufacturers();""",
        )
        manufacturers = [Manufacturer(**row).to_json() for row in result]
        return jsonify(manufacturers), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'error': "Error"}), 500

