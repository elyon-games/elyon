from flask import Blueprint
from common.config import getConfig
route_client = Blueprint("client", __name__)

@route_client.route("/info", methods=["GET"])
def info():
    config = getConfig("server")
    return {
        "version": config["version"],
    }
