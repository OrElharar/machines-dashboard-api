from quart_schema import RequestSchemaValidationError

from utils import logger
from models.custom_exception import CustomException


def errors_handling(app):
    @app.errorhandler(CustomException)
    async def handle_error(error):
        logger.error(error)
        return {"Error": str(error)}, error.status_code

    @app.errorhandler(RequestSchemaValidationError)
    async def handle_request_validation_error(error):
        return {"errors": error.validation_error.json()}, 400

    @app.errorhandler(Exception)
    async def handle_error(error):
        logger.error(error)
        return {"Error": "Error"}, 500

