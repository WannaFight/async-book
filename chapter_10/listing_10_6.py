import functools

from aiohttp import web
import asyncpg

from chapter_10.listing_10_3 import DB_KEY, create_db_pool, destroy_db_pool

routes = web.RouteTableDef()


@routes.get("/products")
async def products(request: web.Request) -> web.Response:
    db: asyncpg.Pool = request.app[DB_KEY]
    products_query = "SELECT product_id, product_name FROM product"
    results = await db.fetch(products_query)
    return web.json_response([dict(record) for record in results])


app = web.Application()
app.on_startup.append(
    functools.partial(
        create_db_pool,
        host="127.0.0.1",
        port=5432,
        user="postgres",
        password="password",
        database="products",
    )
)
app.on_cleanup.append(destroy_db_pool)
