
# services/service_hosts.py
from typing import List, Dict, Any
from .zabbix_service import zabbix_call

def get_extract_hosts( limit: int | None = None, groups: List[str] | None = None,
    query: str | None = None, hostids: List[str] | None = None, ):
    
    params: Dict[str, Any] = {
        "output": ["hostid", "host", "name", "status", "maintenance_status", "maintenanceid"],
        "selectInterfaces": ["interfaceid", "ip", "dns", "port", "error", "available", "main", "type", "useip"],
        "selectGroups": ["groupid", "name"],
        "selectTags": ["tag", "value"],
        "selectInheritedTags": ["tag", "value"],
        "selectInventory": ["location", "hardware", "os", "contact", "type"],
    }
    
    if groups:
        params["groupids"] = groups

    if hostids:
        params["hostids"] = hostids

    if limit:
        params["limit"] = int(limit)

    if query:
        params["search"] = {
            "name": query,
            "host": query,
        }
        params["searchByAny"] = True
        params["searchWildcardsEnabled"] = True
        
    hosts = zabbix_call("host.get", params)
    
    return _normalize_hosts(hosts)

def _normalize_groups(groups):
    out = {
        "customer": None,
        "others": []
    }
    
    for g in groups or []:
        name = g.get("name", "")
        parts = [p.strip() for p in name.split("/") if p.strip()]
        
        root = parts[0].upper()

        if root == "CUSTOMER" and len(parts) >= 2:
            out["customer"] = parts[1]
        else:
            out["others"].append(name)

    return out

def _normalize_os(groups, inventory):
    family = None
    distro = None
    
    for g in groups or []:
        name = g.get("name", "")
        parts = [p.strip() for p in name.split("/") if p.strip()]

        if parts and parts[0].upper() in ("OPERATIONAL_SYSTEM", "OS") and len(parts) >= 2:
            family = parts[1]
            break
    
    if inventory and isinstance(inventory, dict):
        distro = (inventory.get("os") or "").strip() or None
    
    if distro and family:
        return f"{distro} ({family})"

    if family:
        return family

    if distro:
        return distro

    return "-"

def _normalize_customer(groups, tags):
    customer = None
    group_tag = None

    # Customer via grupo
    for g in groups or []:
        name = g.get("name", "")
        parts = [p.strip() for p in name.split("/") if p.strip()]
        if parts and parts[0].upper() == "CUSTOMER" and len(parts) >= 2:
            customer = parts[1]
            break

    # Group via tag
    for t in tags or []:
        if (t.get("tag") or "").strip().lower() == "group":
            group_tag = (t.get("value") or "").strip()
            break

    if customer and group_tag:
        return f"{customer} ({group_tag})"

    if customer:
        return customer

    if group_tag:
        return group_tag

    return "-"

def _normalize_interface(interfaces):
    addresses = set()
    types = set()
    errors = []
    available = 1
    
    for i in interfaces:
        types.add(int(i.get("type", 0)))
        available = min(available, int(i.get("available", 1)))
        
        ip = (i.get("ip") or "").strip()
        dns = (i.get("dns") or "").strip()

        address = ip or dns or "Sem interface"
        
        if address:
            addresses.add(address)

        error = (i.get("error") or "").strip()
        if error:
            errors.append(error)
            
    return {
        "address": sorted(addresses),
        "type": sorted(types),
        "available": available,
        "error": errors
    } 

def _normalize_tags(tags):
    out = {
        "system_id": None,
        "asset_id": None,
        "others": []
    }

    for t in tags or []:
        key = (t.get("tag") or "").strip()
        value = (t.get("value") or "").strip()

        if not key:
            continue

        key_l = key.lower()

        if key_l in ("system id", "system_id", "systemid"):
            out["system_id"] = value

        elif key_l in ("asset id", "asset_id", "assetid"):
            out["asset_id"] = value

        else:
            out["others"].append(f"{key}: {value}")

    return out

def _normalize_hosts(hosts):
    normalize = []
    
    for h in hosts:
        groups = _normalize_groups(h.get("groups", []))
        iface = _normalize_interface(h.get("interfaces", []))
        raw_tags = h.get("tags", []) + h.get("inheritedTags", [])
        tags = _normalize_tags(raw_tags)
        
        inventory = h.get("inventory")
        inventory_type = (
            inventory.get("type")
            if isinstance(inventory, dict) and inventory.get("type")
            else "-"
        )
        
        normalize.append({
                "hostid": int(h["hostid"]),
                "host": h["host"],
                "name": h["name"],
                "status": int(h["status"]),
                "available": int(iface["available"]),
                "maintenance": int(h.get("maintenance_status", 0)) == 1,
                "customer": _normalize_customer(h.get("groups", []), raw_tags),
                "os": _normalize_os(h.get("groups", []), h.get("inventory", {})),
                "system_id": tags["system_id"],
                "asset_id": tags["asset_id"],
                "address": iface["address"],
                "error": iface["error"],
                "host_type": inventory_type,
                "groups": groups.get("others", []),
                "tags": tags["others"],
            })
    
    return normalize