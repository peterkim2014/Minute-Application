from flask import render_template, redirect, request, flash, session
from flask_app import app

@app.route("/evaluation")
def evaluation_home():
    return render_template("evaluation/evaluation_home.html")