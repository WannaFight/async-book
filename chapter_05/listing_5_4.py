import asyncio
from random import sample

import asyncpg


def load_common_words() -> list[str]:
    with open("./data/common_words.txt") as common_words:
        return common_words.readlines()


def generate_brand_names(words: list[str]) -> list[tuple[str]]:
    return [(words[index].strip(),) for index in sample(range(100), 100)]


async def insert_brands(connection, common_words) -> int:
    brands = generate_brand_names(common_words)
    insert_brands = "INSERT INTO brand VALUES(DEFAULT, $1)"
    return await connection.executemany(insert_brands, brands)


async def main():
    common_words = load_common_words()
    connection = await asyncpg.connect(
        host="127.0.0.1",
        port=5432,
        user="postgres",
        password="password",
        database="products",
    )
    await insert_brands(connection, common_words)


asyncio.run(main())
