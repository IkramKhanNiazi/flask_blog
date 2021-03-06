from flask import Flask, request, session, redirect, url_for, \
    render_template, flash, jsonify
from .models import User, Posts, db
from .forms import AddPostForm, SignUpForm, SignInForm, AboutUserForm
from werkzeug.security import check_password_hash, generate_password_hash
from blog import app


@app.route('/')
def index():
    posts_data_list = db.session.query(Posts.pid,
                                       Posts.title, Posts.description,
                                       User.username).filter(
        Posts.puid == User.uid).all()
    return render_template('index.html', posts_data_list=posts_data_list)


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if session['user_available']:
        blog_post = AddPostForm(request.form)
        user = User.query.filter_by(username=session['current_user']).first()
        if request.method == 'POST':
            post = Posts(blog_post.title.data, blog_post.description.data,
                         user.uid)
            db.session.add(post)
            db.session.commit()
            flash('Post Created Succesfully')
            return redirect(url_for('index'))
        return render_template('add.html', blog_post=blog_post)
    flash('User is not Authenticated')
    return redirect(url_for('index'))


@app.route('/delete/<pid>/<post_owner>', methods=('GET', 'POST'))
def delete_post(pid, post_owner):
    if session['current_user'] == post_owner:
        post = Posts.query.get(pid)
        db.session.delete(post)
        db.session.commit()
        flash('Post Deleted Succesfully')
        return redirect(url_for('index'))
    flash('You are not a valid user to Delete this Post')
    return redirect(url_for('index'))


@app.route('/update/<pid>/<post_owner>', methods=('GET', 'POST'))
def update_post(pid, post_owner):
    if session['current_user'] == post_owner:
        post = Posts.query.get(pid)
        blog_post = AddPostForm(obj=post)
        if request.method == 'POST':
            post = Posts.query.get(pid)
            post.title = blog_post.title.data
            post.description = blog_post.description.data
            db.session.commit()
            flash('Post Updated Succesfully')
            return redirect(url_for('index'))
        return render_template('update.html', blog_post=blog_post)
    flash('You are not a valid user to Edit this Post')
    return redirect(url_for('show_posts'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignUpForm(request.form)
    if request.method == 'POST':
        if validate_username(signup_form.username.data) is False:
            flash('Username Already Exists')
            print("Email Invalid")
            return redirect(url_for('signup'))
        if validate_user_email(signup_form.email.data) is False:
            flash('Email Already Exists')
            print("username Invalid")
            return redirect(url_for('signup'))
        else:
            register_user = User(signup_form.username.data,
                                 generate_password_hash(
                                     signup_form.password.data),
                                 signup_form.email.data)
            db.session.add(register_user)
            db.session.commit()
            flash('User Registered Succesfully')
            return redirect(url_for('signin'))
    return render_template('signup.html', signup_form=signup_form)


def validate_user_email(user_email):
    log_user_email = User.query.filter_by(email=user_email).first()
    if log_user_email:
        return False
    else:
        return True


def validate_username(username):
    log_user_username = User.query.filter_by(username=username).first()
    if log_user_username:
        return False
    else:
        return True


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    signin_form = SignInForm(request.form)
    if request.method == 'POST':
        signin_form_email = signin_form.email.data
        log_user = User.query.filter_by(email=signin_form_email).first()
        if log_user:
            if check_password_hash(log_user.password,
                                   signin_form.password.data):
                current_user = log_user.username
                session['current_user'] = current_user
                session['user_available'] = True
                return redirect(url_for('index'))
            else:
                flash('Incorrect Password Entered')
                return render_template('signin.html', signin_form=signin_form)
        else:
            flash('Email Not Registered')
            return render_template('signin.html', signin_form=signin_form)
    return render_template('signin.html', signin_form=signin_form)


@app.route('/logout')
def logout():
    session.clear()
    session['user_available'] = False
    return redirect(url_for('index'))
