import time
from quart import request
from utils import logger


def log_handler(app):
    @app.before_request
    async def log_request():
        logger.info(f"Received request: {request.method} {request.path}")
        request.start_time: float = time.time()

    @app.after_request
    async def log_response(response):
        duration = time.time() - request.start_time if hasattr(request, "start_time") else None
        logger.info(
            f"Request: {request.method} {request.path}, Response: {response.status}, duration_in_seconds: {duration:.4f} ")
        return response
