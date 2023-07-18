from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash

class Ability:

    dB = "minute_app"

    def __init__(self, data):
        self.id = data["id"]
        self.ability = data["ability"]
        self.resume_id = data["resume_id"]
        self.ability_list = []

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO abilities (ability, resume_id) VALUES (%(ability)s, %(resume_id)s);
        """
        result = MySQLConnection(cls.dB).query_db(query, data)

    @classmethod
    def create(cls, data):
        cls.save(data)
        return data

     