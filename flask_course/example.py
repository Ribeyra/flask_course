import random


def app(environ, start_response):
    data = f"random num: {random.randint(0, 1_000_000)}"
    b_data = data.encode('utf-8')
    start_response("404 Not found", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    return iter([b_data])
