from flask import render_template, redirect, request, session
from flask_app import app   
from flask_app.models.user import user
from flask_app.models.show import show
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/shows')
def shows():

    if not session['user_id']:
        return redirect('/')

    data ={
        'id': session['user_id']
    }
    logged_in_user = user.get_by_id(data)
    all_shows = show.get_all_shows()

    return render_template('dashboard.html', user=logged_in_user, shows = all_shows)

@app.route('/add_show', methods=["POST"])
def Create():

    if not session['user_id']:
        return redirect('/')

    if not show.validate_show(request.form):
            return redirect('/add_show')

    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "release_date": request.form["release_date"],
        "network": request.form["network"],
        "user_id": session['user_id']
    }
    show.save(data)
    return redirect('/shows')

@app.route('/add_show')
def add_show():
    if not session['user_id']:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    logged_in_user = user.get_by_id(data)
    return render_template('add_show.html', user=logged_in_user)

@app.route('/shows/<int:id>')
def show_show(id):
    if not session['user_id']:
        return redirect('/')
    data = {
        "id": id,
    }
    selectedshow = show.get_show(data)
    user_data = {
        'id': session['user_id']
    }
    logged_in_user = user.get_by_id(user_data)
    return render_template('view_show.html', show=selectedshow, user=logged_in_user)

@app.route('/shows/edit/<int:id>')
def edit_show(id):
    if not session['user_id']:
        return redirect('/')
    data = {
        "id": id,
    }
    selectedshow = show.get_show(data)
    print(selectedshow.title)
    user_data = {
        'id': session['user_id']
    }
    logged_in_user = user.get_by_id(user_data)
    return render_template('edit_show.html', show=selectedshow, user=logged_in_user)

@app.route('/shows/destroy/<int:id>')
def delete_show(id):
    if not session['user_id']:
        return redirect('/')
    data = {
        "id": id,
    }

    show.delete(data)
    return redirect('/shows')

@app.route('/Update_show/<int:id>', methods=["POST"])
def Update_show(id):
    if not session['user_id']:
        return redirect('/')
    if not show.validate_show(request.form):
            return redirect('/shows/edit/' + str(id))
    
    data = {
        'id': id,
        "title": request.form["title"],
        "description": request.form["description"],
        "release_date": request.form["release_date"],
        "network": request.form["network"],
        "user_id": session['user_id']
    }
    show.Update(data)
    return redirect('/shows')