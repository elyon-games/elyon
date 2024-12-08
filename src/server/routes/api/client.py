from flask import Blueprint
from server.services.config import configData
route_client = Blueprint("client", __name__)

@route_client.route("/info", methods=["GET"])
def info():
    print(configData)
    return {
        "version": configData["version"],
    }
