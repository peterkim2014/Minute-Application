from flask import render_template, request, redirect, flash, session
from flask_app.models.company import Company
from flask_app.models.application import Application
from flask_app.models.qualification import Qualification
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/company_login_page")
def company_login_page():
    return render_template("company/company_login.html")

@app.route("/company_register")
def company_register_page():
    return render_template("company/company_register.html")

@app.route("/company_home")
def company_homepage():
    
    return render_template("company/company_homepage.html")

@app.route("/company_applications")
def application_view():
    company_id = session["user_id"]

    if Application.get_all_by_company_id(company_id):
        applications = Application.get_all_by_company_id(company_id)
        company = Company.get_company_by_id(company_id)
        for application in applications:

            qualifications = Qualification.get_qualification_by_application_id(application.id)

            return render_template("company/application_company.html", applications=applications, company=company, qualifications=qualifications)
    
    return render_template("company/application_company.html")

@app.route("/application/edit/<int:id>")
def application_edit_form(id):
    company_id = session["user_id"]

    if Application.get_company_by_id(id):
        application = Application.get_company_by_id(id)

        qualifications = Application.get_qualification_by_application(id)

    return render_template("company/application_edit.html", application=application, id=id, qualifications=qualifications)

@app.route("/application/edit", methods=["POST"])
def application_edit():
    user_id = session["user_id"]

    if Application.validate_application(request.form):
        data = {
            "position": request.form["position"],
            "position_overview": request.form["position_overview"],
            "position_role": request.form["position_role"],
            "due_day": request.form["due_day"],
            "due_time": request.form["due_time"],
            "id": request.form["id"]
        }
        Application.update_application(data)

    return redirect("/company_applications")


@app.route("/application_add")
def application_form():
    company_id = session["user_id"]
    company = Company.get_company_by_id(company_id)
    
    return render_template("company/application_add.html", company=company)

@app.route("/application_add_form", methods=["POST"])
def initiate_application_form():
    user_id = session["user_id"]

    if Application.validate_application(request.form):
        data = {
            "position": request.form["position"],
            "position_overview": request.form["position_overview"],
            "position_role": request.form["position_role"],
            "due_day": request.form["due_day"],
            "due_time": request.form["due_time"],
            "company_id": request.form["company_id"]
        }
        Application.create(data)
        flash("Thank you for submitting your application")
        return redirect("company_home")
    else:
        return redirect("application_add"), flash("Invalid Form")


@app.route("/company_register_form", methods=["POST"])
def company_form():
    if Company.validate_registration(request.form):
        data = {
            "name": request.form["name"],
            "industry": request.form["industry"],
            "brief": request.form["brief"],
            "email": request.form["email"],
            "password": bcrypt.generate_password_hash(request.form["password"])
        }
        Company.create(data)
        flash("Thank you for registering")
        return redirect("company_login_page"), flash("Thank you for registering")
    else:
        return redirect("company_register")

@app.route("/company_login", methods=["POST"])
def company_login():

    user = Company.get_company_by_email(request.form["email"])
    print(user)

    if user == None or bcrypt.check_password_hash(user.password, request.form["password"]) == False:
        flash("Invalid Credentials", "login")
        return redirect("company_login_page")

    session["user_id"] = user.id
    flash("Login Successful")
    return redirect("/company_home")