from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.application import Application
from flask_app.models.resume import Resume
from flask_app.models.company import Company
from flask_app.models.ability import Ability
from flask_app.models.user import User

@app.route("/account")
def account_page():
    user_id = session["user_id"]
    user = User.get_by_id(user_id)
    resume = Resume.get_resume_by_id(user.id)

    if Resume.get_resume_by_id(user_id):
        resumes = Resume.get_resume_by_id(user_id)
        resume_abilities = Resume.get_abilities_by_resume(resumes.id)

        return render_template("account/account_home.html", resumes=resumes, resume_abilities=resume_abilities, user=user)
    return render_template("account/account_home.html")

@app.route("/add_attributes", methods=["POST"])
def submit_attributes():
    user_id = session["user_id"]
    data = {
        "pitch": request.form["pitch"],
        "education": request.form["education"],
        "position": request.form["position"],
        "user_id": user_id
    }
    Resume.create(data)

    return redirect("/account")

@app.route("/edit_attributes", methods=["POST"])
def edit_attributes():
    user_id = session["user_id"]
    user = User.get_by_id(user_id)
    resume = Resume.get_resume_by_id(user.id)
    data = {
        "pitch": request.form["pitch"],
        "education": request.form["education"],
        "position": request.form["position"],
        "user_id": user_id,
        "id": resume.id
    }
    Resume.edit(data)

    return redirect("/account")

@app.route("/add_ability", methods=["POST"])
def add_ability_form():
    user_id = session["user_id"]
    user_resume = Resume.get_resume_by_user(user_id)
    data = {
        "ability": request.form["ability"],
        "resume_id": user_resume.id
    }
    Ability.create(data)


    return redirect("/account") 