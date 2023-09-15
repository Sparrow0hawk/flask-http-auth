import functools

from flask import Flask, request

app = Flask(__name__)


def check_auth(username, password):
    return username == "foo" and password == "magic"


def login_required(f):
    @functools.wraps(f)
    def decorated_func(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return (
                "Unauthorized",
                401,
                {"WWW-Authenticate": "Basic realm='Login Required'"},
            )
        return f(*args, **kwargs)

    return decorated_func


@app.route("/")
@login_required
def index() -> str:
    return "<h1>Hello World!</h1>"
