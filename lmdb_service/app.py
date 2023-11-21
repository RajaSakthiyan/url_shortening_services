import os
from marshmallow import Schema, ValidationError, fields

from flask import Flask, abort, request
from lib.db import DBOperation

NOT_ALLOWED_DOMAINS = ("https://sho.rt/",)


app = Flask(__name__)
app_settings = os.getenv("APP_SETTINGS", "lib.settings.DevelopmentConfig")
app.config.from_object(app_settings)
db_operation = DBOperation(app)


class PayloadSchema(Schema):
    hash = fields.String(required=True)
    code = fields.String(required=True)
    long_url = fields.String(required=True)


payload_schema = PayloadSchema()


@app.route("/put", methods=("POST",))
def put() -> tuple[list, int]:
    try:
        post_data: dict = payload_schema.load(request.get_json())
        data: dict | None = db_operation.put_data(post_data)
        if data:
            return (
                payload_schema.dump(data),
                201,
            )
        abort(500)
    except ValidationError as e:
        abort(422)


@app.route("/get/<alias_code>", methods=("GET",))
def get(alias_code) -> tuple[list, int]:
    try:
        data: dict | None = db_operation.get_data(alias_code)
        if data:
            return (
                payload_schema.dump(data),
                200,
            )
        abort(500)
    except ValidationError as e:
        abort(422)


@app.errorhandler(422)
@app.errorhandler(500)
def handle_error(error: Exception):
    return (
        payload_schema.dump({"hash": None, "code": None, "long_url": None}),
        error.code,
    )
