import os
from quart import Quart
from quart_schema import QuartSchema
from quart_jwt_extended import JWTManager
from quart_cors import cors
from middlewares import errors, log, db_connection
from .config import config

app = Quart(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
auth_manager = JWTManager(app)

QuartSchema(app)
app.config.update(config)
app = cors(
    app,
    allow_origin="http://localhost:3000",
    allow_methods=["OPTIONS", "GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    allow_credentials=True,
)

db_connection.db_connection_handler(app)

log.log_handler(app)

errors.errors_handling(app)





