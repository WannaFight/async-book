import asyncpg
from aiohttp.web import Application

DB_KEY = "database"


async def create_db_pool(
    app: Application,
    host: str,
    port: int,
    user: str,
    password: str,
    database: str,
):
    pool = await asyncpg.create_pool(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        min_size=6,
        max_size=6,
    )
    app[DB_KEY] = pool


async def destroy_db_pool(app: Application):
    pool: asyncpg.Pool = app[DB_KEY]
    await pool.close()
