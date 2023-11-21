import os
from marshmallow import Schema, ValidationError, fields

from flask import Flask, abort, request
from flask_cors import CORS

from lib.db import RemoteLMDB, DBError

NOT_ALLOWED_DOMAINS = ("https://sho.rt/", "http://localhost/", "http://127.0.0.1/")
URL_CHAR_MAX = 2040


app = Flask(__name__)
app_settings = os.getenv("APP_SETTINGS", "lib.settings.DevelopmentConfig")
app.config.from_object(app_settings)
lmdb = RemoteLMDB(app)
CORS(app)


class ShortUrlSchema(Schema):
    long_url = fields.Url(required=True, load_only=True)
    status = fields.String(dump_only=True)
    message = fields.String(dump_only=True)
    alias: fields.Nested(
        Schema.from_dict(
            dict(id=fields.String(), code=fields.String(), long_url=fields.String())
        ),
        dump_only=True,
    )


short_url_schema = ShortUrlSchema()


@app.route("/create_short_url", methods=("POST",))
def create_short_url() -> tuple[list, int]:
    try:
        post_data: dict = short_url_schema.load(request.get_json())
        if post_data["long_url"] in NOT_ALLOWED_DOMAINS:
            abort(422, "The given URL domain is restricted in our service")
        elif len(post_data["long_url"]) >= URL_CHAR_MAX:
            abort(414, "The given URL is too long for the server to proceed")
        result = lmdb.create_alias(post_data["long_url"])
        return (
            short_url_schema.dump(
                dict(
                    status="success", message="Short url has been created", alias=result
                )
            ),
            201,
        )
    except ValidationError as e:
        abort(422, e)
    except DBError as e:
        abort(500, e)


@app.errorhandler(414)
@app.errorhandler(422)
@app.errorhandler(500)
def handle_error(error: Exception):
    return short_url_schema.dump({"status": "error", "message": str(error)}), error.code
