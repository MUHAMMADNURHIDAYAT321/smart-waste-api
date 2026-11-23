
from flask import Blueprint, request
from controllers.controller import (
    MODELS,
    get_all,
    get_one,
    create,
    update,
    delete,
    error
)

api = Blueprint("api", __name__)


@api.route("/<resource>", methods=["GET", "POST"])
def collection(resource):

    if resource not in MODELS:
        return error("Endpoint tidak ditemukan", 404)

    if request.method == "POST":
        return create(resource)

    return get_all(resource)


@api.route(
    "/<resource>/<int:item_id>",
    methods=["GET", "PUT", "DELETE"]
)
def detail(resource, item_id):

    if resource not in MODELS:
        return error("Endpoint tidak ditemukan", 404)

    if request.method == "PUT":
        return update(resource, item_id)

    if request.method == "DELETE":
        return delete(resource, item_id)

    return get_one(resource, item_id)