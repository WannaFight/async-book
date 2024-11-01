import logging
from http import HTTPStatus

import asyncpg
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from asyncpg.pool import Pool

routes = web.RouteTableDef()

DB_KEY = "database"


async def create_db_pool(app: web.Application):
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
    app[DB_KEY] = pool


async def destroy_db_pool(app: web.Application):
    logging.info("destroying db pool...")
    pool: Pool = app.pop(DB_KEY)
    await pool.close()


@routes.get("/brands")
async def brands_list(request: Request) -> Response:
    connection: Pool = request.app[DB_KEY]
    brands_query = "SELECT brand_id, brand_name FROM brand"
    results: list[asyncpg.Record] = await connection.fetch(brands_query)
    results_as_dict: list[dict] = [dict(brand) for brand in results]

    return web.json_response(results_as_dict)


@routes.get("/products/{id}")
async def get_product(request: Request) -> Response:
    try:
        product_id = int(request.match_info["id"])
    except ValueError:
        raise web.HTTPBadRequest()

    query = """
        SELECT
            product_id,
            product_name,
            brand_id
        FROM
            product
        WHERE
            product_id = $1"""
    connection: Pool = request.app[DB_KEY]
    result: asyncpg.Record = await connection.fetchrow(query, product_id)

    if result is None:
        raise web.HTTPNotFound()

    return web.json_response(dict(result))


@routes.post("/products")
async def create_product(request: Request) -> Response:
    PRODUCT_NAME = "product_name"
    BRAND_ID = "brand_id"

    if not request.can_read_body:
        raise web.HTTPBadRequest(reason="empty body")

    body = await request.json()

    if PRODUCT_NAME not in body or BRAND_ID not in body:
        raise web.HTTPBadRequest(
            reason=f"`{PRODUCT_NAME}` and `{BRAND_ID}` are required"
        )

    connection: Pool = request.app[DB_KEY]
    await connection.execute(
        "INSERT INTO product(product_id, product_name, brand_id) VALUES(DEFAULT, $1, $2)",
        body[PRODUCT_NAME],
        int(body[BRAND_ID]),
    )
    return web.Response(status=HTTPStatus.CREATED)


app = web.Application()
app.on_startup.append(create_db_pool)
app.on_cleanup.append(destroy_db_pool)

app.add_routes(routes)
web.run_app(app)
