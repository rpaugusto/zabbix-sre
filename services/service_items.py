# services/service_items.py
from typing import List, Dict, Any
from .zabbix_service import zabbix_call

def list_agents_by_group(groupid: str) -> List[Dict[str, Any]]:
    
    hosts = zabbix_call("host.get", {
        "groupids": groupid,
        "output": ["hostid", "host"],
    })
    
    results = []
    
    for h in hosts:
        items = zabbix_call("item.get", {
            "hostids": h["hostid"],
            "output": ["itemid", "name", "key_", "lastvalue"],
            "search": {"name": "agent"},   # exemplo simplificado
        })
        
        results.append({
            "host": h["host"],
            "items": items
        })
    
    return results
