import asyncio
import logging
from typing import Awaitable

import aiohttp
from aiohttp import web

routes = web.RouteTableDef()

PRODUCT_BASE = "127.0.0.1:8000"
INVENTORY_BASE = "127.0.0.1:8001"
FAVORITE_BASE = "127.0.0.1:8002"
CART_BASE = "127.0.0.1:8003"


@routes.get("/products/all")
async def all_products(request: web.Request) -> web.Response:
    async with aiohttp.ClientSession() as session:
        products = asyncio.create_task(session.get(f"{PRODUCT_BASE}/products"))
        favorites = asyncio.create_task(
            session.get(f"{FAVORITE_BASE}/users/3/favorties")
        )
        cart = asyncio.create_task(session.get(f"{CART_BASE}/users/3/cart"))

        requests = [products, favorites, cart]
        done, pending = await asyncio.wait(requests, timeout=1.0)

        if products in pending:
            for req in requests:
                req.cancel()
            return web.json_response(
                {"error": "could not reach products service"}, status=504
            )

        elif products in done and products.exception() is not None:
            for req in requests:
                req.cancel()
            logging.exception(
                "server error reaching products service", exc_info=products.exception()
            )
            return web.json_response(
                {"error": "server error reaching products service"}, status=500
            )

        products_response = await products.result().json()
        products_results = await get_products_with_inventory(session, products_response)
        cart_item_count = await get_response_item_count(
            cart, done, pending, "Error getting user cart."
        )
        favorites_item_count = await get_response_item_count(
            favorites, done, pending, "Error getting user favorties"
        )

    return web.json_response(
        {
            "cart_items": cart_item_count,
            "favorite_items": favorites_item_count,
            "products": products_results,
        }
    )


async def get_products_with_inventory(
    session: aiohttp.ClientSession,
    products: web.Response,
) -> list[dict]:
    def get_inventory(session: aiohttp.ClientSession, product_id: str) -> asyncio.Task:
        url = f"{INVENTORY_BASE}/products/{product_id}/inventory"
        return asyncio.create_task(session.get(url))

    def create_product_record(product_id: int, inventory: int | None) -> dict:
        return {"product_id": product_id, "inventory": inventory}

    inventory_tasks_to_product_id = {
        get_inventory(session, product["product_id"]): product["product_id"]
        for product in products
    }

    inv_done, inv_pending = await asyncio.wait(
        inventory_tasks_to_product_id.keys(), timeout=1.0
    )
    products_results = []
    for done_task in inv_done:
        if done_task.exception() is None:
            product_id = inventory_tasks_to_product_id[done_task]
            inv = await done_task.result().json()
            products_results.append(create_product_record(product_id, inv["inventory"]))
        else:
            product_id = inventory_tasks_to_product_id[done_task]
            products_results.append(create_product_record(product_id, None))
            logging.exception(
                "error getting inventory for id=%s",
                product_id,
                exc_info=inventory_tasks_to_product_id[done_task].exception(),
            )

    for pending_task in inv_pending:
        pending_task.cancel()
        product_id = inventory_tasks_to_product_id[pending_task]
        products_results.append(create_product_record(product_id, None))

    return products_results


async def get_response_item_count(
    task: asyncio.Task, done: set[Awaitable], pending: set[Awaitable], error_msg: str
) -> int | None:
    if task in done and task.exception() is None:
        return len(await task.result().json())
    elif task in pending:
        task.cancel()
    else:
        logging.exception(error_msg, exc_info=task.exception())
