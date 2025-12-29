
from flask import render_template

def index():
    return render_template("home.html", title="Bem-vindo ao Zabbix Helper")