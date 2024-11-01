from asyncio import Future
import asyncio


def make_request() -> Future:
    print("inside make_request")
    future = Future()
    task = asyncio.create_task(set_future_value(future))
    print(f"set task {task} for future {future}")
    return future


async def set_future_value(future: Future) -> None:
    sleep_for = 2
    print(f"inside set_future_value, sleep for {sleep_for} seconds")
    await asyncio.sleep(sleep_for)
    future.set_result(42)
    print("result has been set")


async def main():
    future = make_request()
    print(f"is the future done? {future.done()}")
    value = await future
    print(f"is the future done? {future.done()}")
    print(f"future result: {value}")


asyncio.run(main())
