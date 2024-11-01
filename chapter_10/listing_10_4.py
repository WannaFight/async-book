import functools

import asyncpg
from aiohttp import web

from chapter_10.listing_10_3 import DB_KEY, create_db_pool, destroy_db_pool

routes = web.RouteTableDef()


@routes.get("/users/{id}/favorites")
async def favorites(request: web.Request) -> web.Response:
    try:
        user_id = int(request.match_info["id"])
    except ValueError:
        raise web.HTTPBadRequest()

    db: asyncpg.Pool = request.app[DB_KEY]
    favorites_query = "SELECT product_id FROM user_favorite WHERE user_id = $1"

    result = await db.fetch(favorites_query, user_id)
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
        database="favorites",
    )
)
app.on_cleanup.append(destroy_db_pool)

app.add_routes(routes)
web.run_app(app, port=8002)
