import asyncio
import logging
import asyncpg


async def main():
    connection: asyncpg.Connection = await asyncpg.connect(
        host="127.0.0.1",
        port=5432,
        user="postgres",
        password="password",
        database="products",
    )
    try:
        async with connection.transaction():
            await connection.execute("INSERT INTO brand VALUES(9999, 'big_brand')")
            await connection.execute("INSERT INTO brand VALUES(9999, 'big_brand')")
    except Exception:
        logging.exception("Error while running transactions")
    finally:
        query = """SELECT brand_name FROM brand
                    WHERE brand_name LIKE 'big%'"""

        brands = await connection.fetch(query)
        print(brands)

        await connection.close()


asyncio.run(main())
