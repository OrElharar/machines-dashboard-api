from databases import Database


async def create_db_connection(app) -> Database:
    db = Database(app.config['DATABASE_URL'])
    await db.connect()
    return db


