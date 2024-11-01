import asyncio


async def cor_add_one(number: int) -> int:
    return number + 1


cor_result = asyncio.run(cor_add_one(1))

print(f"Coroutine result is {cor_result} and the type is {type(cor_result)}")
