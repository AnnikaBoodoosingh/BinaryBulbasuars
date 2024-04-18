from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from App.models import*
from.index import index_views

from App.controllers import (
    login
)

from App.controllers import signup
from App.database import db



auth_views = Blueprint('auth_views', __name__, template_folder='../templates')


'''
Page/Action Routes
'''    
@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")
    

@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    token = login(data['username'], data['password'])
    if not token:
        flash('Bad username or password given'), 401
        response = redirect(request.referrer)
    else:
        flash('Login Successful')
        response = redirect('/homePage')
        set_access_cookies(response, token) 
    return response

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect('/loginPage') 
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response

@auth_views.route('/signup', methods=['POST'])
def signup_action():
    data = request.form
    token, message = signup(data['username'], data['password'])
    if not token:
        flash(message), 401
        return redirect(request.referrer)  
    flash('Signup Successful')
    response = redirect('/loginPage')  
    set_access_cookies(response, token) 
    return response

@auth_views.route('/signupPage', methods=['GET'])
def signup_page():
    return render_template('signupPage.html')

@auth_views.route('/loginPage', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_views.route('/homePage', methods=['GET'])
def home_page():
    return render_template('layout.html')
    
@auth_views.route('/browseWorkoutsPage')
def browse_workouts_page():
    workouts = Workout.query.all()
    return render_template('browseWorkouts.html', workouts=workouts)

@auth_views.route('/workout/<int:id>')
def workout_details(id):
    selected_workout = Workout.query.get(id)
    return render_template('workoutDetails.html', selected_workout=selected_workout)

@auth_views.route('/myRoutinesPage')
def myRoutines_page():
    workouts = Workout.query.all()
    return render_template('myRoutines.html', workouts=workouts)

'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = login(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  response = jsonify(access_token=token) 
  set_access_cookies(response, token)
  return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response

@auth_views.route('/api/signup', methods=['POST'])
def user_signup_api():
    data = request.json
    token, message = signup(data['username'], data['password'])
    if not token:
        return jsonify(message=message), 401
    response = jsonify(access_token=token, message='Signup Successful')
    set_access_cookies(response, token)
    return response
