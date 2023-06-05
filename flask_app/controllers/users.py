from flask import render_template, redirect, request, session
from flask_app import app   
from flask_app.models.user import user
# from flask_app.models.show import show
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    session['user_id'] = None
    return render_template('index.html')

@app.route('/register_user', methods=["POST"])
def register_user():

    if not user.validate_user(request.form):
        return redirect('/')

    pw_hash=bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }

    user_id = user.save(data)
    session['user_id'] = user_id
    return redirect('/shows')

@app.route('/log_in_user', methods = ["POST"])
def log_in_user():

    login_data = {
        "email": request.form["email"],
        "password": request.form["password"]
    }

    if not user.valirelease_date_login(login_data):
        return redirect('/')

    data = {
        "email": request.form["email"],
    }
    usr = user.get_user_by_email(data)
    if not bcrypt.check_password_hash( usr.password , request.form['password']):
        return redirect('/')

    session['user_id'] = usr.id
    return redirect('/shows')