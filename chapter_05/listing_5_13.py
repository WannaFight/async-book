import asyncio
import asyncpg


async def main():
    connection: asyncpg.Connection = await asyncpg.connect(
        host="127.0.0.1",
        port=5432,
        user="postgres",
        password="password",
        database="products",
    )

    query = "SELECT product_id, product_name FROM product"
    async with connection.transaction():
        cursor = await connection.cursor(query)
        await cursor.forward(500)  # skip first 500 rows
        products = await cursor.fetch(100)  # saelect 100 rows
        for product in products:
            print(product)

    await connection.close()


asyncio.run(main())
