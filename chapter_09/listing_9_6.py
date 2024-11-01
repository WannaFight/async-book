import logging

import asyncpg
from asyncpg import Pool, Record
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route


async def create_db_pool():
    logging.info("creating database pool...")
    pool: Pool = await asyncpg.create_pool(
        host="127.0.0.1",
        port=5432,
        user="postgres",
        password="password",
        database="products",
        min_size=6,
        max_size=6,
    )
    app.state.DB = pool


async def destroy_db_pool():
    logging.info("destroying db pool...")
    pool = app.state.DB
    await pool.close()


async def brands(request: Request) -> JSONResponse:
    connection: Pool = request.app.state.DB
    brands_query = "SELECT brand_id, brand_name FROM brand"
    results: list[Record] = await connection.fetch(brands_query)
    results_as_dict = [dict(brand) for brand in results]

    return JSONResponse(results_as_dict)


app = Starlette(
    routes=[Route("/brands", brands)],
    on_startup=[create_db_pool],
    on_shutdown=[destroy_db_pool],
)
