from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.show import show
from flask_bcrypt import Bcrypt        
from flask_app import app
bcrypt = Bcrypt(app)
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class user:

    def __init__(self, data):
        self.id = data ['id']
        self.first_name = data ['first_name']
        self.last_name = data ['last_name']
        self.email = data ['email']
        self.password = data ['password']
        self.created_at = data ['created_at']
        self.updated_at = data ['updated_at']
        self.shows = []


    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name, last_name, email, password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s, %(email)s, %(password)s, NOW() , NOW() );"
        
        return connectToMySQL('Shows').query_db( query, data )

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email= %(email)s ;"
        results =  connectToMySQL('Shows').query_db(query, data)
        return cls(results[0])


    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users LEFT JOIN shows ON users.id=shows.user_id WHERE users.id= %(id)s ;"
        results =  connectToMySQL('Shows').query_db(query, data)

        if not results:
            return None

        User = user(results[0])

        for row in results:
            if row['shows.id']:
                User.shows.append(show({
                    "id": row['shows.id'],
                    "title": row['title'],
                    "description" : row['description'],
                    "release_date": row['release_date'],
                    "network": row['network'],
                    "created_at": row['shows.created_at'],
                    "updated_at": row['shows.updated_at'],
                    "user_id": row['user_id'],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                }))

        return User

    @staticmethod
    def validate_user(user):
        is_valid = True 
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(user['last_name']) < 1:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if len(user['password']) < 8:
            flash("password must be at least 8 characters.")
            is_valid = False
        if not user['confirm_password'] == user['password']:
            flash("passwords must match.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid

    @staticmethod
    def valirelease_date_login(user):
        is_valid = True 
        if len(user['email']) < 1:
            flash("Email required.")
            is_valid = False
        if len(user['password']) < 1:
            flash("Password required.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid