from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash

class Qualification:

    dB = "minute_app"

    def __init__(self, data):
        self.id = data["id"]
        self.qualification = data["qualification"]
        self.application_id = data["application_id"]
        self.qualification_list = []

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO qualifications (qualification, application_id) VALUES (%(qualification)s, %(application_id)s);
        """
        result = MySQLConnection(cls.dB).query_db(query, data)

    @classmethod
    def create(cls, data):
        cls.save(data)
        return data

    @classmethod
    def get_qualification_by_application_id(cls, id):
        query = """
            SELECT * FROM qualifications WHERE application_id = %(id)s;
        """
        results = MySQLConnection(cls.dB).query_db(query, {"id":id})
        if results:
            qualification_list = []
            for result in results:
                qualification = cls(result)
                qualification.qualification_list = qualification
                qualification_list.append(qualification)
            return qualification_list
        return None
