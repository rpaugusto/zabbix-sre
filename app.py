# app.py
from flask import Flask, request, session
from config import Config
from routes import bp as main_bp
import datetime
import flask
import os


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    @app.context_processor
    def inject_globals():
        # Detecta ambiente (compatível com Flask antigo e novo)
        env = os.getenv("FLASK_ENV") or app.config.get("ENV", "production")
        env = str(env).lower()

        is_dev = env in ("development", "dev", "local")

        # Proteção defensiva para session["user"]
        user = session.get("user")
        role = user.get("role") if isinstance(user, dict) else None

        can_admin = is_dev or role == "admin"

        return {
            "app_name": app.config.get("APP_NAME", "Zabbix Helper"),
            "current_year": datetime.datetime.now().year,
            "flask_version": flask.__version__,
            "is_dev": is_dev,
            "can_admin": can_admin,
            "request_path": request.path,
        }

    app.register_blueprint(main_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        port=5000,
        debug=True,
    )
