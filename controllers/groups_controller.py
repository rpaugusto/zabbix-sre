
from flask import render_template, request, Response
from services.service_groups import list_groups, group_detail, export_group_hosts_csv
from io import StringIO
import csv

def index():
    data = list_groups()
    return render_template("groups.html", title="Grupos", groups=data)

def detail():
    groupid = request.args.get("id")
    d = group_detail(groupid) if groupid else {"hosts": []}
    return render_template("groups.html", title="Grupo Detalhe", detail=d)

def export_group_hosts():
    groupid = request.args.get("id", "")
    rows = export_group_hosts_csv(groupid)
    si = StringIO()
    writer = csv.writer(si)
    writer.writerows(rows)
    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": f'attachment; filename=group_{groupid}_hosts.csv'}
    )
