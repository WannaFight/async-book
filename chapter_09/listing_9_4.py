# Simple WSGI app


def application(env, start_response):
    # dict of gunicorn env variables, like method, socket, remote_addr etc.
    print("env", type(env), env)
    # gunicorn.http.wsgi.Response.start_response
    print("start_response", type(start_response), start_response)
    start_response("200 OK", [("Content-Type", "text/html")])
    return [b"WSGI hello!"]
