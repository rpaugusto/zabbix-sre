
# routes.py
from flask import Blueprint
from controllers import (
    home_controller, zabbix_controller, config_controller,
    hosts_controller, templates_controller, groups_controller
)

bp = Blueprint("main", __name__)

# === Registrar rotas aqui ===
bp.add_url_rule("/", view_func=home_controller.index, methods=["GET"])

#bp.add_url_rule("/zabbix/test", view_func=zabbix_controller.test, methods=["GET"])

bp.add_url_rule("/config", view_func=config_controller.index, methods=["GET"])
bp.add_url_rule("/config", view_func=config_controller.update, methods=["POST"])

#bp.add_url_rule("/hosts", view_func=hosts_controller.index, methods=["GET"])
#bp.add_url_rule("/hosts/detail", view_func=hosts_controller.detail, methods=["GET"])
#bp.add_url_rule("/hosts/export", view_func=hosts_controller.export, methods=["GET"])
#
#bp.add_url_rule("/templates", view_func=templates_controller.index, methods=["GET"])
#
#bp.add_url_rule("/groups", view_func=groups_controller.index, methods=["GET"])
#bp.add_url_rule("/groups/detail", view_func=groups_controller.detail, methods=["GET"])
#bp.add_url_rule("/groups/export/csv", view_func=groups_controller.export_group_hosts, methods=["GET"])

