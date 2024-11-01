import asyncio
import asyncpg

from util import async_timed


product_query = """
SELECT
    p.product_id,
    p.product_name,
    p.brand_id,
    s.sku_id,
    pc.product_color_name,
    ps.product_size_name
FROM product AS p
JOIN sku AS s USING(product_id)
JOIN product_color AS pc USING(product_color_id)
JOIN product_size AS ps USING(product_size_id)
WHERE p.product_id = 100
"""


async def query_product(pool: asyncpg.Pool):
    async with pool.acquire() as connection:
        return await connection.fetchrow(product_query)


@async_timed()
async def query_products_sync(pool: asyncpg.Pool, queries: int):
    return [await query_product(pool) for _ in range(queries)]


@async_timed()
async def query_products_conc(pool: asyncpg.Pool, queries: int):
    queries = [query_product(pool) for _ in range(queries)]
    return await asyncio.gather(*queries)


async def main():
    async with asyncpg.create_pool(
        host="127.0.0.1",
        port=5432,
        user="postgres",
        password="password",
        database="products",
        min_size=6,
        max_size=6,
    ) as pool:
        await query_products_sync(pool, 10000)
        await query_products_conc(pool, 10000)


asyncio.run(main())
