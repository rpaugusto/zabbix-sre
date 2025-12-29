
# services/service_hosts.py
from typing import List, Dict, Any
from .zabbix_service import zabbix_call

def list_hosts() -> List[Dict[str, Any]]:

    result = zabbix_call("host.get", {
        "output": ["hostid", "host", "status"],
        "selectGroups": ["groupid", "name"],
        "selectInterfaces": ["ip", "type"],
    })

    hosts = []
    for h in result:
        groups = [g["name"] for g in h.get("groups", [])]
        status = "OK" if str(h.get("status", "0")) == "0" else "DISABLED"
        hosts.append({
            "id": int(h["hostid"]),
            "name": h["host"],
            "status": status,
            "groups": groups,
            "ip": (h.get("interfaces") or [{}])[0].get("ip"),
        })
    return hosts

def host_detail(hostid: str) -> Dict[str, Any]:
    res = zabbix_call("host.get", {
        "hostids": hostid,
        "output": "extend",
        "selectGroups": "extend",
        "selectParentTemplates": ["templateid", "name"],
        "selectInterfaces": "extend",
    })
    if not res:
        return {}

    h = res[0]
    return {
        "id": int(h["hostid"]),
        "name": h["host"],
        "status": "OK" if str(h.get("status", "0")) == "0" else "DISABLED",
        "groups": [{"id": g["groupid"], "name": g["name"]} for g in h.get("groups", [])],
        "templates": [{"id": t["templateid"], "name": t["name"]} for t in h.get("parentTemplates", [])],
        "interfaces": h.get("interfaces", []),
    }

def export_hosts_csv() -> List[List[str]]:

    data = list_hosts()
    header = ["ID", "Nome", "Status", "Grupos", "IP"]
    rows = [header]
    for h in data:
        rows.append([
            str(h["id"]),
            h["name"],
            h["status"],
            ", ".join(h["groups"]),
            h.get("ip") or "",
        ])
    return rows
