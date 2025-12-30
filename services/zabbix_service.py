
# services/zabbix_service.py
import requests
from typing import Any, Dict
from flask import current_app

class ZabbixError(Exception):
    pass

def zabbix_call(method: str, params: Dict[str, Any], auth: bool = True) -> Any:

    URL = current_app.config.get("ZABBIX_API_URL", "")
    TOKEN = current_app.config.get("ZABBIX_TOKEN", "")

    if not URL or not TOKEN:
        raise ZabbixError("ZABBIX_API_URL ou ZABBIX_TOKEN não configurados.")

    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
    }
    
    if auth:
        if not TOKEN:
            raise ZabbixError("ZABBIX_TOKEN não configurado.")
        payload["auth"] = "8e23cb57a408645e992b6a42933f936fddac8fc86a6016a3ad76912ba593e705" #TOKEN

    try:
        resp = requests.post(URL, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        raise ZabbixError(f"Falha HTTP na chamada '{method}': {e}") from e
    except ValueError:
        raise ZabbixError("Resposta não é JSON válido.")

    if "error" in data:
        err = data["error"]
        raise ZabbixError(f"Zabbix erro {err.get('code')}: {err.get('message')} - {err.get('data')}")

    return data.get("result")