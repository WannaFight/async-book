import asyncio
import asyncpg
import asyncpg.transaction


async def main():
    connection: asyncpg.Connection = await asyncpg.connect(
        host="127.0.0.1",
        port=5432,
        user="postgres",
        password="password",
        database="products",
    )

    transaction: asyncpg.transaction.Transaction = connection.transaction()
    await transaction.start()

    try:
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'ultra_brand_1')")
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'ultra_brand_2')")
    except asyncpg.PostgresError:
        print("Errors, rolling back transaction!")
        await transaction.rollback()
    else:
        print("No errors, commiting transaction!")
        await transaction.commit()

    query = """SELECT brand_name FROM brand WHERE brand_name LIKE 'ultra_brand%'"""
    brands = await connection.fetch(query)
    print(brands)

    await connection.close()


asyncio.run(main())
