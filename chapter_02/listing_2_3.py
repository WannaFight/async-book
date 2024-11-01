import asyncio


async def add_one(number: int) -> int:
    print(f"called with {number}")
    return number + 1


async def main() -> None:
    print("main start")
    one_plus_one = await add_one(1)
    print("first await")
    one_plus_two = await add_one(2)
    print("second await")
    print(one_plus_one)
    print(one_plus_two)


asyncio.run(main())
