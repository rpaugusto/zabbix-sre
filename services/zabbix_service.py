
# services/zabbix_service.py
import requests
from typing import Any, Dict
from flask import current_app

class ZabbixError(Exception):
    pass

def zabbix_call(method: str, params: Dict[str, Any]) -> Any:

    URL = current_app.config.get("ZABBIX_API_URL", "")
    TOKEN = current_app.config.get("ZABBIX_TOKEN", "")

    if not URL or not TOKEN:
        raise ZabbixError("ZABBIX_API_URL ou ZABBIX_TOKEN não configurados.")

    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
        "auth": TOKEN,  # com API Token, o auth é o próprio token
    }

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