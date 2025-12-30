
# routes.py

from flask import Blueprint
from helpers import login_required
from controllers import (
    home_controller, zabbix_controller, config_controller,
    hosts_controller, templates_controller, groups_controller, auth_controller
)

bp = Blueprint("main", __name__)

# LOGIN
bp.add_url_rule("/login", view_func=auth_controller.login, methods=["GET", "POST"], endpoint="login")
bp.add_url_rule("/logout", view_func=auth_controller.logout, methods=["GET"], endpoint="logout")

# === Registrar rotas aqui ===
bp.add_url_rule("/", view_func=login_required(home_controller.index), methods=["GET"], endpoint="home_index")

bp.add_url_rule("/config", view_func=config_controller.index, methods=["GET"], endpoint="config_index")
bp.add_url_rule("/config", view_func=config_controller.update, methods=["POST"], endpoint="config_update")
bp.add_url_rule("/config/test", view_func=config_controller.test_connection, methods=["POST"], endpoint="config_test")

bp.add_url_rule("/hosts", view_func=hosts_controller.index, methods=["GET"], endpoint="host_index")
#bp.add_url_rule("/hosts/detail", view_func=hosts_controller.detail, methods=["GET"])
#bp.add_url_rule("/hosts/export", view_func=hosts_controller.export, methods=["GET"])

#bp.add_url_rule("/templates", view_func=templates_controller.index, methods=["GET"])

#bp.add_url_rule("/groups", view_func=groups_controller.index, methods=["GET"])
#bp.add_url_rule("/groups/detail", view_func=groups_controller.detail, methods=["GET"])
#bp.add_url_rule("/groups/export/csv", view_func=groups_controller.export_group_hosts, methods=["GET"])

