from datetime import timedelta
from quart_jwt_extended import create_access_token


def generate_token(token_payload):
    token = create_access_token(token_payload, expires_delta=timedelta(hours=12))
    return token
