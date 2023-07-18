from flask_app import app
from flask_app.controllers import users, applications, calenders, evaluations, minutes, company, accounts, qualifications

if __name__=="__main__":
    app.run(debug=True)