from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash
from flask_app.models.ability import Ability

class Resume:

    dB = "minute_app"

    def __init__(self, data):
        self.id = data["id"]
        self.pitch = data["pitch"]
        self.education = data["education"]
        self.position = data["position"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.ability_list = []

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO resumes (pitch, education, position, user_id) VALUES (%(pitch)s, %(education)s, %(position)s, %(user_id)s);
        """
        result = MySQLConnection(cls.dB).query_db(query, data)

    @classmethod
    def create(cls, data):
        cls.save(data)
        return data
    
    @classmethod
    def edit(cls, data):
        query = """
            UPDATE resumes SET pitch = %(pitch)s, education = %(education)s, position = %(position)s WHERE id = %(id)s; 
        """
        results = MySQLConnection(cls.dB).query_db(query, data)
    
    @classmethod
    def get_resume_by_id(cls, id):
        query = """
            SELECT * FROM resumes WHERE id = %(id)s;
        """
        results = MySQLConnection(cls.dB).query_db(query, {"id": id})
        return cls(results[0]) if results else None 
    

    @classmethod
    def get_abilities_by_resume(cls, id):
        query = """
            SELECT * FROM resumes LEFT JOIN abilities ON resumes.id = abilities.resume_id WHERE resumes.id = %(id)s;
        """
        results = MySQLConnection(cls.dB).query_db(query,{"id":id})
        if results:
            abilities_response = []
            for result in results:
                ability_data = {
                    "id": result["id"],
                    "ability": result["ability"],
                    "resume_id": result["resume_id"]
                }
                ability_cls = Ability(ability_data)
                resume = cls(result)
                resume.ability_list = ability_cls
                abilities_response.append(resume)
            return abilities_response
        return None
    
    @classmethod
    def get_resume_by_user(cls, id):
        query = """
            SELECT * FROM resumes WHERE user_id = %(id)s;
        """     
        results = MySQLConnection(cls.dB).query_db(query,{"id":id})
        return cls(results[0]) if results else None