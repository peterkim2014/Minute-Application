from flask import render_template, request, redirect, flash, session
from flask_app.models.company import Company
from flask_app.models.application import Application
from flask_app.models.qualification import Qualification
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/qualifications/add", methods=["POST"])
def add_qualification():

    data = {
        "qualification": request.form["qualification"],
        "application_id": request.form["application_id"]
    }
    print(data)
    Qualification.create(data)

    return redirect("/company_applications")