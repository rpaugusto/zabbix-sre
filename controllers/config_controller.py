#controllers/config_controller.py

from flask import render_template, request, current_app, redirect, url_for, jsonify
from helpers import csrf_verify, flash_set
from services.zabbix_service import zabbix_call, ZabbixError

def index():
    return render_template(
        "config.html",
        title="Configuração",
        zabbix_url=current_app.config.get("ZABBIX_API_URL", ""),
        has_token=bool(current_app.config.get("ZABBIX_TOKEN"))
    )

def update():
    token = request.form.get("_token")

    if not csrf_verify(token):
        flash_set("danger", "CSRF inválido.")
        return redirect(url_for("main.config_index"))

    zabbix_url = request.form.get("zabbix_url", "").strip()
    zabbix_token = request.form.get("zabbix_token", "").strip()

    if zabbix_url:
        current_app.config["ZABBIX_API_URL"] = zabbix_url

    if zabbix_token:
        current_app.config["ZABBIX_TOKEN"] = zabbix_token

    flash_set("success", "Configurações atualizadas (somente em memória).")
    return redirect(url_for("main.config_index"))


def test_connection():
    data = request.get_json() or {}

    zabbix_url = data.get("zabbix_url", "").strip()
    zabbix_token = data.get("zabbix_token", "").strip()

    if not zabbix_url and not current_app.config.get("ZABBIX_API_URL"):
        return jsonify(success=False, message="Zabbix URL não informada."), 400

    if not zabbix_token and not current_app.config.get("ZABBIX_TOKEN"):
        return jsonify(success=False, message="Zabbix Token não informado."), 400

    # Backup config atual
    old_url = current_app.config.get("ZABBIX_API_URL")
    old_token = current_app.config.get("ZABBIX_TOKEN")

    try:
        # Injeta temporariamente para o teste
        if zabbix_url:
            current_app.config["ZABBIX_API_URL"] = zabbix_url
        if zabbix_token:
            current_app.config["ZABBIX_TOKEN"] = zabbix_token

        version = zabbix_call("apiinfo.version", {}, auth=False)

        return jsonify(
            success=True,
            message=f"Conexão realizada com sucesso (Zabbix {version})."
        )

    except ZabbixError as e:
        return jsonify(success=False, message=str(e)), 400

    finally:
        # Restaura config original
        current_app.config["ZABBIX_API_URL"] = old_url
        current_app.config["ZABBIX_TOKEN"] = old_token