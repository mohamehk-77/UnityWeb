#!/usr/bin/python3
from flask import Flask, request, redirect, url_for, render_template, flash
from api.v1.views import *
from Create import add_user, check_password_hash, Users, Posts, session
app = Flask(__name__)

app.register_blueprint(User_app_views, url_prefix='/api/v1')
app.register_blueprint(Post_app_views, url_prefix='/api/v1')
app.register_blueprint(Comment_app_views, url_prefix='/api/v1')
app.register_blueprint(Like_app_views, url_prefix='/api/v1')
app.register_blueprint(Follow_app_views, url_prefix='/api/v1')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        profile_name = request.form['profile_name']
        email = request.form['email']
        password = request.form['password']
        birthday = request.form['birthday']
        add_user(first_name, last_name, gender, profile_name, email, password, birthday)
        return redirect(url_for('home'))
    return render_template('signin_Page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Store user ID in session
            flash('You were successfully logged in')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('login'))
    return render_template('login_Page.html')


@app.route('/home')
def home():
    if 'user_id' not in session:
        flash('Please log in to view this page')
        return redirect(url_for('login'))
    posts = Posts.query.all()
    return render_template('home.html', posts=posts)





if __name__ == '__main__':
    app.run(debug=True)
