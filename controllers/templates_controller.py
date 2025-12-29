
from flask import render_template
from services.service_templates import list_templates

def index():
    data = list_templates()

    return render_template("templates_page.html", title="Templates", templates=data)
