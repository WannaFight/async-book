# Simple ASGI app


async def application(scope, receive, send):
    # dict, some metadata
    print("scope", type(scope), scope)
    # uvicorn.lifespan.on.LifespanOn.receive
    print("receive", type(receive), receive)
    # uvicorn.lifespan.on.LifespanOn.send
    print("send", type(send), send)
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"text/html"]],
        }
    )
    await send({"type": "http.response.body", "body": b"ASGI hello!"})
