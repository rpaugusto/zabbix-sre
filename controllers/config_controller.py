
from flask import render_template, request, current_app, redirect, url_for
from helpers import csrf_verify, flash_set

def index():

    cfg = {
        "ZABBIX_API_URL": current_app.config.get("ZABBIX_API_URL", ""),
        "ZABBIX_TOKEN": "***" if current_app.config.get("ZABBIX_TOKEN") else "",
    }

    return render_template("config.html", title="Configuração", config=cfg)

def update():
    token = request.form.get("_token")

    if not csrf_verify(token):
        flash_set("danger", "CSRF inválido.")
        return redirect(url_for("main.config"))

    url = request.form.get("ZABBIX_API_URL", "")
    current_app.config["ZABBIX_API_URL"] = url

    flash_set("success", "Config atualizada (somente em memória).")

    return redirect(url_for("main.config"))
