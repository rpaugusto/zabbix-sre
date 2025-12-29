
from flask import jsonify
from services.zabbix_service import zabbix_call

def test():
    # chamada simples para verificar conexão
    res = zabbix_call("apiinfo.version", {})
    return jsonify({"api_version": res})
