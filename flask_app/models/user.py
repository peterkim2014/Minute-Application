import re
from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9,+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:

    dB = "minute_app"

    def __init__(self, user_data):
        self.id = user_data["id"]
        self.first_name = user_data["first_name"]
        self.last_name = user_data["last_name"]
        self.email = user_data["email"]
        self.password = user_data["password"]
        self.created_at = user_data["created_at"]
        self.updated_at = user_data["updated_at"]

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        result = MySQLConnection(cls.dB).query_db(query, data)

    @classmethod
    def create(cls, data):
        cls.save(data)
        return data
    
    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM users;
        """
        result = MySQLConnection(cls.dB).query_db(query)
        return result

    @classmethod
    def get_by_id(cls, id):
        query = """
            SELECT * FROM users WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        print(cls(result[0]) if result else None)
        return cls(result[0]) if result else None

    @classmethod
    def get_by_email(cls, email):
        query = """
            SELECT * FROM users WHERE email = %(email)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"email": email})
        print(cls(result[0]) if result else None)
        return cls(result[0]) if result else None

    @classmethod
    def update_email(cls, id):
        query = """
            UPDATE users SET email = %{email}s WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        print(cls(result[0]) if result else None)
        return cls(result[0]) if result else None

    @classmethod
    def update_password(cls, id):
        query = """
            UPDATE users SET password = %{password}s WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        print(cls(result[0]) if result else None)
        return cls(result[0]) if result else None
    
    @classmethod
    def delete(cls, id):
        query = """
            SELECT * FROM users WHERE id = %{id}s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        return result        

    @staticmethod
    def validate_registration(user):
        is_valid = True

        if len(user["password"]) < 3:
            is_valid = False
            flash("Password is too short", "registration")
        if user["password"] != user["confirm_password"]:
            is_valid = False
            flash("Password does not match", "registration")
        if User.get_by_email(user["email"]):
            is_valid = False
            flash("Email address already used", "registration")
        if not EMAIL_REGEX.match(user["email"]):
            is_valid = False
            flash("Invalid Email Address", "registration")

        return is_valid
