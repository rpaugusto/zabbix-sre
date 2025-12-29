# services/service_groups.py
from typing import List, Dict, Any
from .zabbix_service import zabbix_call

def list_groups() -> List[Dict[str, Any]]:

    res = zabbix_call("hostgroup.get", {
        "output": ["groupid", "name"]
    })

    return [{"id": int(g["groupid"]), "name": g["name"]} for g in res]

def group_detail(groupid: str) -> Dict[str, Any]:

    hosts = zabbix_call("host.get", {
        "groupids": groupid,
        "output": ["hostid", "host", "status"],
    })

    return {
        "groupid": int(groupid),
        "hosts": [{
            "id": int(h["hostid"]),
            "name": h["host"],
            "status": "OK" if str(h.get("status", "0")) == "0" else "DISABLED",
        } for h in hosts]
    }

def export_group_hosts_csv(groupid: str) -> List[List[str]]:
    
    detail = group_detail(groupid)
    
    header = ["Host ID", "Host", "Status"]
    rows = [header]

    for h in detail["hosts"]:
        rows.append([str(h["id"]), h["name"], h["status"]])

    return rows

