from flask import render_template, request, redirect, url_for, session

ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin123"

def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USER and password == ADMIN_PASSWORD:
            session["user"] = username
            return redirect(url_for("main.home_index"))
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)

def logout():
    session.clear()
    return redirect(url_for("auth.login"))