from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9,+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Company:

    dB = "minute_app"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.industry = data["industry"]
        self.brief = data["brief"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO companies (name, industry, brief, email, password) VALUES (%(name)s, %(industry)s, %(brief)s, %(email)s, %(password)s);
        """
        result = MySQLConnection(cls.dB).query_db(query, data)

    @classmethod
    def create(cls, data):
        cls.save(data)
        return data
    
    @classmethod
    def get_company_by_id(cls, id):
        query = """
            SELECT * FROM companies WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        return cls(result[0]) if result else None
    
    @classmethod
    def get_company_by_email(cls, email):
        query = """
            SELECT * FROM companies WHERE email = %(email)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"email": email})
        return cls(result[0]) if result else None


    @classmethod
    def validate_registration(cls, user):
        is_valid = True

        if len(user["name"]) < 3:
            is_valid = False
            flash("Please fill in business name", "registration")
        if len(user["brief"]) < 1:
            is_valid = False
            flash("Please fill in company brief", "registration")
        if len(user["password"]) < 3:
            is_valid = False
            flash("Password is too short", "registration")
        if user["password"] != user["confirm_password"]:
            is_valid = False
            flash("Password does not match", "registration")
        if cls.get_company_by_email(user["email"]):
            is_valid = False
            flash("Email address already used", "registration")
        if not EMAIL_REGEX.match(user["email"]):
            is_valid = False
            flash("Invalid Email Address", "registration")

        return is_valid

    @classmethod
    def validate_application(cls, application):
        is_valid = True

        if len(application["position"]) < 1:
            is_valid = False
            flash("Please fill in position", "registration")
        if len(application["position_overview"]) < 1:
            is_valid = False
            flash("Please fill in position overview", "registration")
        if len(application["position_qualifications"]) < 1:
            is_valid = False
            flash("Please fill in position qualifications", "registration")
        if len(application["application_due"]) < 1:
            is_valid = False
            flash("Please fill in application due", "registration")

        return is_valid
    
