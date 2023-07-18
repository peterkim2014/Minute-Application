from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.resume import Resume
from flask_app.models.user import User
from flask_app.models.application import Application
from flask_app.models.calender import Calender

@app.route("/calender")
def calender_home():

    return render_template("calender/calender_home.html")

@app.route("/calender/add/<int:id>")
def calender_add(id):
    user_id = session["user_id"]
    user = User.get_by_id(user_id)
    
    if Resume.get_resume_by_user(user_id):
        resume = Resume.get_resume_by_user(user_id)


        return render_template("calender/calender_add.html", resume=resume, user=user, application_id=id)
    return render_template("calender/calender_add.html")

@app.route("/interview_add", methods=["POST"])
def add_interview():
    user_id = session["user_id"]
    user = User.get_by_id(user_id)
    data = {
        "interview_day": request.form["interview_day"],
        "interview_time": request.form["interview_time"],
        "application_id": request.form["application_id"],
        "resume_id": request.form["resume_id"],
        "user_id": user.id
    }
    Calender.create(data)

    return redirect("/calender")