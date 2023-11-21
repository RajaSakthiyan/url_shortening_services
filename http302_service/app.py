import os
from flask import Flask, abort, redirect

from lib.db import RemoteLMDB


app = Flask(__name__)
app_settings = os.getenv("APP_SETTINGS", "lib.settings.DevelopmentConfig")
app.config.from_object(app_settings)
lmdb = RemoteLMDB(app)


@app.route("/<alias_code>", methods=("GET",))
def create_short_url(alias_code) -> tuple[list, int]:
    try:
        result = lmdb.get_long_url(alias_code)
        if result["long_url"]:
            return redirect(result["long_url"], 302)
        abort(404)
    except Exception:
        abort(404)
