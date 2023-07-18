from flask_app.config.mysqlconnection import MySQLConnection

class Calender:

    dB = "minute_app"

    def __init__(self, data):
        self.id = data["id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = None
        self.application_id = None
        self.company_id = None

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO calenders (interview_day, interview_time, user_id, application_id, resume_id) VALUES (%(interview_day)s, %(interview_time)s, %(user_id)s,%(application_id)s, %(resume_id)s);
        """
        result = MySQLConnection(cls.dB).query_db(query, data)

    @classmethod
    def create(cls, data):
        cls.save(data)
        return data
    
    @classmethod
    def get_calenders(cls):
        query = """
            SELECT * FROM calenders;
        """
        result = MySQLConnection(cls.dB).query_db(query)
        return result
    
    @classmethod
    def get_all(cls, data):
        query = """
            SELECT * FROM calenders 
            LEFT JOIN companies ON companies.id = calenders.company_id 
            LEFT JOIN applications ON applications.id = calenders.application_id 
            LEFT JOIN users ON users.id = calenders.user_id 
            WHERE applications.id = %(application_id)s
            AND calenders.user_id=%()s;
        """