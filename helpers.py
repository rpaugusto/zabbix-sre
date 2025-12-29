
# helpers.py
from flask import flash, redirect, url_for, session, request
import os, secrets

def env(key: str, default=None):
    return os.getenv(key, default)

def config_get(app, key: str, default=None):
    # acessa app.config['CHAVE1.CHAVE2'] -> simples: só plano
    return app.config.get(key, default)

def csrf_token() -> str:
    t = session.get("_csrf_token")
    if not t:
        t = secrets.token_hex(16)
        session["_csrf_token"] = t
    return t

def csrf_field() -> str:
    return f'<input type="hidden" name="_token" value="{csrf_token()}">'

def csrf_verify(token: str | None) -> bool:
    sess = session.get("_csrf_token", "")
    return token is not None and sess and secrets.compare_digest(sess, token)

def flash_set(msg_type: str, message: str):
    # tipos: success, warning, danger, info...
    flash(message, msg_type)

def flash_get_all():
    # no Flask, templates usam get_flashed_messages(category_filter=[...])
    pass

def base_url(endpoint="home", **kwargs):
    return url_for(endpoint, **kwargs)

def asset(path: str):
    # use url_for('static', filename='...')
    return url_for("static", filename=path)

def redirect_to(endpoint: str, **kwargs):
    return redirect(url_for(endpoint, **kwargs))