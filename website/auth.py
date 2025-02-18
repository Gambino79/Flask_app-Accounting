from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email=request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, please try again', category='error')
        else:
            print(user)
            flash('The email is not registered.', category='error')    
        
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/reset_password', methods=['GET', 'POST'])
def pwreset():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        
        if user is None:
            flash('This email does not exist', category='error')
        elif password1 != password2:
            flash('The two passwords are not the equal.', category='error')
        elif len(password1) < 8:
            flash('The password must be at leat 8 characters long.', category='error')
        else:
            # update the password
            password=generate_password_hash(password1, method='pbkdf2:sha256')
            user.password = password
            db.session.commit()
            return redirect(url_for('auth.login'))
        
    return render_template("reset_password.html", user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email='email').first()
        
        if user:
            flash('This email is already registered', category='error')
        elif len(email) < 10:
            flash('Email must be greater than 9 characters.', category='error')
        elif len(first_name) < 5:
            flash('First Name must be greater than 4 characters.', category='error')
        elif len(last_name) <5:
            flash('Last Name must be greater than 4 characters.', category='error')
        elif password1 != password2:
            flash('The two passwords are not the equal.', category='error')
        elif len(password1) < 8:
            flash('The password must be at leat 8 characters long.', category='error')
        else:
            # add user to database
            new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            flash('Account added with success', category='success')
            
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('The account has been created', category='success')
            return redirect(url_for('auth.login'))
        
    return render_template("singup.html", user=current_user)