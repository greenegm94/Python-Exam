from math import isnan
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class show:

    def __init__(self, data):
        self.id = data ['id']
        self.title = data ['title']
        self.description = data ['description']
        self.release_date = data ['release_date']
        self.network = data ['network']
        self.user_id = data ['user_id']
        self.created_at = data ['created_at']
        self.updated_at = data ['updated_at']
        
        self.first_name = data ['first_name']
        self.last_name = data ['last_name']
        self.email = data ['email']


    @classmethod
    def get_all_shows(cls):
        query = "SELECT * FROM shows LEFT JOIN users ON shows.user_id=users.id;"
        results =  connectToMySQL('Shows').query_db(query)
        if not results:
            return None

        shows = []
        for r in results:
            shows.append(cls(r))
        return shows

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO shows ( title, description, release_date, network, user_id, created_at, updated_at ) VALUES ( %(title)s, %(description)s, %(release_date)s, %(network)s , %(user_id)s, NOW() , NOW());"
        
        return connectToMySQL('Shows').query_db( query, data )

    @classmethod
    def get_show(cls, data):

        query = "SELECT * FROM shows LEFT JOIN users ON users.id=shows.user_id WHERE shows.id= %(id)s ;"

        result =  connectToMySQL('Shows').query_db(query, data)

        if not result:
            return None

        return show(result[0])


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM shows WHERE id=%(id)s;"

        results =  connectToMySQL('Shows').query_db(query, data)
        return results

    @classmethod
    def Update(cls, data ):
        query = "Update shows SET title=%(title)s, description=%(description)s, network=%(network)s, release_date=%(release_date)s, user_id=%(user_id)s, updated_at=NOW() WHERE id = %(id)s;"
        
        return connectToMySQL('Shows').query_db( query, data )

    @staticmethod
    def validate_show(show):
        is_valid = True 
        if len(show['title']) < 3:
            flash("Title must be at least 3 characters.")
            is_valid = False
        if len(show['description']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False
        if len(show['release_date']) < 1:
            flash("Release Date required.")
            is_valid = False
        if len(show['network']) < 3:
            flash("Network must be at least 3 characters.")
            is_valid = False

        return is_valid