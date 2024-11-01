from asyncio import Future

my_future = Future()

print(f"is future done? {my_future.done()}")

my_future.set_result(42)

print(f"is future done? {my_future.done()}")
print(f"what is the result of future? {my_future.result()}")
