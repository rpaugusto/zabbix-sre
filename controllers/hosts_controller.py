
from flask import render_template, request, Response
from services.service_hosts import list_hosts, host_detail, export_hosts_csv
import csv
from io import StringIO

def index():
    data = list_hosts()

    return render_template("hosts.html", title="Hosts", hosts=data)

def detail():
    hostid = request.args.get("id")
    data = host_detail(hostid) if hostid else {}

    return render_template("hosts.html", title="Host Detalhe", host=data)

def export():
    rows = export_hosts_csv()
    si = StringIO()
    writer = csv.writer(si)
    writer.writerows(rows)
    output = si.getvalue()

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=hosts.csv"})
