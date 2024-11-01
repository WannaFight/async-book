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

    async with connection.transaction():
        # 1 transaction, save point
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'my_new_brand')")

        try:
            # 2 transaction, will fail and will be rolled back
            async with connection.transaction():
                await connection.execute(
                    "INSERT INTO  product_color VALUES(1, 'black')"
                )
        except Exception as ex:
            logging.warning("Ignoring  error inserting product color", exc_info=ex)

    await connection.close()


asyncio.run(main())
