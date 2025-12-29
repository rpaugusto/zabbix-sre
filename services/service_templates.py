# services/service_templates.py
from typing import List, Dict, Any
from .zabbix_service import zabbix_call

def list_templates() -> List[Dict[str, Any]]:
    res = zabbix_call("template.get", {
        "output": ["templateid", "name", "description"],
        "selectGroups": ["groupid", "name"],
        "limit" : 5,
    })
    
    return [{
        "id": int(t["templateid"]),
        "name": t["name"],
        "groups": [g["name"] for g in t.get("groups", [])],
        "description": t.get("description") or "",
    } for t in res]