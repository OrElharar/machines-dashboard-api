from db import create_db_connection


def db_connection_handler(app):
    @app.before_serving
    async def create_db_pool():
        app.db = await create_db_connection(app)

    @app.after_serving
    async def close_db_pool():
        await app.db.disconnect()
