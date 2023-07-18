from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.application import Application
from flask_app.models.company import Company
from flask_app.models.resume import Resume
from flask_app.models.ability import Ability
from flask_app.models.user import User

@app.route("/homepage")
def homepage():
    user_id = session["user_id"]
    user = User.get_by_id(user_id)

    if Resume.get_resume_by_id(user_id):
        resumes = Resume.get_resume_by_id(user_id)
        resume_abilities = Resume.get_abilities_by_resume(resumes.id)
        if Application.get_application_by_user(user_id):
            applications = Application.get_application_by_user(user_id)
            for application in applications:
                company_id = application.company_id
                company = Company.get_company_by_id(company_id)
                return render_template("main/homepage.html", resumes=resumes, resume_abilities=resume_abilities, user=user, applications=applications, company=company)
        else:
            return render_template("main/homepage.html", resumes=resumes, resume_abilities=resume_abilities, user=user)

        
    return render_template("main/homepage.html")

@app.route("/applications")
def application_home():
    user_id = session["user_id"]

    if Application.get_all():
        applications = Application.get_all()
        
        for application in applications:
            company_id = application["company_id"]
            company = Company.get_company_by_id(company_id)
            if Application.get_application_by_user(user_id):
                application_added = Application.get_application_by_user(user_id)

                return render_template("application/application_home.html", applications=applications, company=company, application_added=application_added, user_id=user_id)
            else:
                return render_template("application/application_home.html", applications=applications, company=company, user_id=user_id, application_added=None)
    
    return render_template("application/application_home.html")

@app.route("/my_applications")
def my_application_view():
    user_id = session["user_id"]
    my_applications = Application.get_application_by_user(user_id)
    company_id = None
    if my_applications != None:
        for application in my_applications:
            company_id = application.company_id
            company = Company.get_company_by_id(company_id)
            return render_template("application/application_view.html", my_applications=my_applications, company=company)

    return render_template("application/application_view.html")


@app.route("/application_add/<int:id>")
def application_add_user(id):
    user_id = session["user_id"]
    data = {
        "user_id": user_id,
        "application_id": id
    }
    Application.application_add(data)
    return redirect("/applications")

@app.route("/application_remove/<int:id>")
def application_remove_user(id):
    data = {
        "user_id": None,
        "application_id": id
    }
    Application.application_add(data)
    return redirect("/applications")