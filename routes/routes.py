from quart import Blueprint, request, jsonify
from .account import account_router
from .machines import machines_router
from .images import images_router
from .manufacturers import manufacturers_router

routes = Blueprint('api', __name__)

routes.register_blueprint(account_router, url_prefix='/accounts')
routes.register_blueprint(machines_router, url_prefix='/machines')
routes.register_blueprint(images_router, url_prefix='/images')
routes.register_blueprint(manufacturers_router, url_prefix='/manufacturers')
