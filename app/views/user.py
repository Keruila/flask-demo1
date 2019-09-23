from flask import Blueprint

user = Blueprint("user", __name__)


@user.route("/")
def index():
    return "我是新来的用户"
