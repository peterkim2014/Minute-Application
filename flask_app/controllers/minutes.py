from flask import render_template, redirect, request, flash, session
from flask_app import app

@app.route("/minute")
def minute_home():
    return render_template("minute/minute_home.html")

@app.route("/minute/inbox")
def minute_inbox():
    return render_template("minute/minute_inbox.html")