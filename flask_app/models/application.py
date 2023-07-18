from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash
from flask_app.models.company import Company
from flask_app.models.user import User
from flask_app.models.qualification import Qualification

class Application:

    dB = "minute_app"

    def __init__(self, data):
        self.id = data["id"]
        self.position = data["position"]
        self.position_overview = data["position_overview"]
        self.position_role = data["position_role"]
        self.due_day = data["due_day"]
        self.due_time = data["due_time"]
        self.company_id = data["company_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.applications = []
        self.applications_all = []
        self.application_user = []
        self.calender_id = None
        self.position_qualifications = []

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO applications (position, position_overview, position_role, company_id) VALUES (%(position)s, %(position_overview)s, %(position_role)s, %(company_id)s);
        """
        result = MySQLConnection(cls.dB).query_db(query, data)

    @classmethod
    def get_qualification_by_application(cls, id):
        query = """
            SELECT * FROM applications LEFT JOIN qualifications ON applications.id = qualifications.application_id WHERE applications.id = %(id)s;
        """
        results = MySQLConnection(cls.dB).query_db(query,{"id":id})
        if results:
            position_qualifications = []
            for result in results:
                qualification_data = {
                    "id": result["id"],
                    "qualification": result["qualification"],
                    "application_id": result["application_id"]
                }
                qualification_cls = Qualification(qualification_data)
                application = cls(result)
                application.qualification_list = qualification_cls
                position_qualifications.append(application)
            return position_qualifications
        return None

    @classmethod
    def update_application(cls, data):
        query = """
            UPDATE applications SET position = %(position)s, position_overview = %(position_overview)s, position_role = %(position_role)s, due_day = %(due_day)s, due_time = %(due_time)s WHERE id = %(id)s;
        """
        results = MySQLConnection(cls.dB).query_db(query, data)

    @classmethod
    def create(cls, data):
        cls.save(data)
        return data
    
    @classmethod
    def application_add(cls, data):
        query = """
            UPDATE applications SET user_id = %(user_id)s WHERE id = %(application_id)s;
        """
        results = MySQLConnection(cls.dB).query_db(query, data)

    @classmethod
    def get_application_by_id(cls, id):
        query = """
            SELECT * FROM application WHERE id = %(id)s;
        """
        results = MySQLConnection(cls.dB).query_db(query, {"id":id})
        return cls(results[0]) if results else None

    @classmethod
    def get_application_by_user(cls, id):
        query = """
            SELECT * FROM applications LEFT JOIN users ON applications.user_id = users.id WHERE users.id = %(id)s; 
        """
        results = MySQLConnection(cls.dB).query_db(query, {"id": id})
        if results:
            application_user = []
            for result in results:
                user_data = {
                    "id": result["id"],
                    "first_name": result["first_name"],
                    "last_name": result["last_name"],
                    "email": result["email"],
                    "password": result["password"],
                    "created_at": result["created_at"],
                    "updated_at": result["updated_at"],
                }
                user = User(user_data)
                application = cls(result)
                application.application_user = user
                application_user.append(application)
            # print(application_user)
            return application_user
        return None
    
    @classmethod
    def get_all_by_company_id(cls, id):
        query = """
            SELECT * FROM applications LEFT JOIN companies ON companies.id = applications.company_id WHERE applications.company_id = %(id)s;
        """
        results = MySQLConnection(cls.dB).query_db(query, {"id": id})
        if results:
            applications = []
            for result in results:
                company_data = {
                    "id": result["id"],
                    "name": result["name"],
                    "industry": result["industry"],
                    "brief": result["brief"],
                    "email": result["email"],
                    "password": None,
                    "created_at": None,
                    "updated_at": None
                }
                company_info = Company(company_data)
                application = cls(result)
                application.applications = company_info
                applications.append(application)
            return applications
        return None
    
    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM applications;
        """
        results = MySQLConnection(cls.dB).query_db(query)
        return results
    
    @classmethod
    def get_company_by_id(cls, id):
        query = """
            SELECT * FROM applications WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        return cls(result[0]) if result else None
    
    @classmethod
    def get_company_by_email(cls, email):
        query = """
            SELECT * FROM applications WHERE email = %(email)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"email": email})
        return cls(result[0]) if result else None

    @classmethod
    def validate_application(cls, application):
        is_valid = True

        if len(application["position"]) < 1:
            is_valid = False
            flash("Please fill in position", "registration")
        if len(application["position_overview"]) < 1:
            is_valid = False
            flash("Please fill in position overview", "registration")
        if not len(application["due_day"]):
            is_valid = False
            flash("Please fill in application due", "registration")
        if not len(application["due_time"]):
            is_valid = False
            flash("Please fill in application due", "registration")

        return is_valid
    
