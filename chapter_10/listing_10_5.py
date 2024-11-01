import functools
from aiohttp import web
import asyncpg

from chapter_10.listing_10_3 import DB_KEY, create_db_pool, destroy_db_pool

routes = web.RouteTableDef()


@routes.get("/users/{id}/cart")
async def user_cart(request: web.Request) -> web.Response:
    try:
        user_id = int(request.match_info["id"])
    except ValueError:
        raise web.HTTPBadRequest()

    db: asyncpg.Pool = request.app[DB_KEY]
    cart_query = "SELECT product_id FROM user_cart WHERE user_id = $1"
    result = await db.fetch(cart_query, user_id)

    if result is None:
        raise web.HTTPNotFound()

    return web.json_response([dict(record) for record in result])


app = web.Application()
app.on_startup.append(
    functools.partial(
        create_db_pool,
        host="127.0.0.1",
        port=5432,
        user="postgres",
        password="password",
        database="cart",
    )
)
app.on_cleanup.append(destroy_db_pool)

app.add_routes(routes)
web.run_app(app, port=8003)
