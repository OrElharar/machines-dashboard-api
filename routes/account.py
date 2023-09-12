from quart import jsonify, Blueprint
from quart_schema import validate_request
from services import tokens_service
from app.app import app
from services.case_converter import to_camel_case_mapper
from entities.login import LoginInputDTO
from entities.user import User

account_router = Blueprint('account', __name__)


@account_router.route('/login', methods=['POST'])
@validate_request(LoginInputDTO)
async def login(data: LoginInputDTO):
    """Login."""
    result = await app.db.fetch_all(
        """SELECT * from select_user_by_username(:username);""",
        values={'username': data.username},
    )
    users = [User(**row) for row in result]
    if len(users) == 0:
        return jsonify({'error': 'Access Denied'}), 401
    user = users[0]
    if user.password != data.password:
        return jsonify({'error': 'Access Denied'}), 401

    token = tokens_service.generate_token({'id': user.id, 'username': data.username})
    response = to_camel_case_mapper({"token": token, "username": user.username, "full_name": user.full_name})
    return response, 200
