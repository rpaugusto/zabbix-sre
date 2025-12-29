
# controllers/items_controller.py
from flask import jsonify, request
from services.service_items import list_agents_by_group

def export_agents_by_group():
    groupid = request.args.get("id")
    data = list_agents_by_group(groupid)

    return jsonify(data)
