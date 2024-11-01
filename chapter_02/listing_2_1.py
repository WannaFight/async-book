async def cor_add_one(number: int) -> int:
    return number + 1


def add_one(number: int) -> int:
    return number + 1


function_result = add_one(1)
cor_result = cor_add_one(1)

print(f"Function result is {function_result} and the type is {type(function_result)}")
print(f"Coroutine result is {cor_result} and the type is {type(cor_result)}")
