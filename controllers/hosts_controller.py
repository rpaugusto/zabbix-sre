# controllers/hosts_controller.py

from flask import render_template, request, Response
from services.service_hosts import get_extract_hosts
from io import StringIO
import csv

def index():
    query = request.args.get("q")
    limit = request.args.get("limit", 100)

    data = []
    error = None
    
    if query:
        try:
            data = get_extract_hosts(
                query=query,
                limit=limit
            )
        except Exception as e:
            error = str(e)
            
    return render_template(
        "hosts_index.html", hosts=data, 
        query=query, error=error )

def detail():
    hostid = request.args.get("id")

    if not hostid:
        return render_template(
            "hosts_detail.html",
            title="Host não encontrado",
            host=None
        )

    hosts = get_extract_hosts(hostids=[hostid])

    host = hosts[0] if hosts else None

    return render_template(
        "hosts_detail.html",
        title=f"Host {host.get('name') if host else ''}",
        host=host
    )


def export():
    query = request.args.get("q")

    hosts = get_extract_hosts(query=query)

    si = StringIO()
    writer = csv.writer(si)

    # Header
    writer.writerow([
        "HostID",
        "Host",
        "Name",
        "Customer",
        "OS",
        "Available",
        "Maintenance",
        "Address",
        "Groups",
        "Tags",
    ])

    for h in hosts:
        writer.writerow([
            h["hostid"],
            h["host"],
            h["name"],
            h["customer"],
            h["os"],
            h["available"],
            h["maintenance"],
            ", ".join(h["address"]),
            ", ".join(h["groups"]),
            ", ".join(h["tags"]),
        ])

    output = si.getvalue()

    return Response(
        output,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=hosts.csv"
        }
    )