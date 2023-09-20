import secrets
import os
from PIL import Image

from flask import render_template, flash, redirect, url_for, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.Form import LogInForm, SingUPForm, UpdateAccountForm, PostForm
from flaskblog.modules import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all()
    return render_template('home.html', 
                           posts=posts,
                           title ='Home Page')

@app.route('/about')
def about():
    return render_template('about.html',
                           title='About Page')


@app.route('/registration', methods=['GET','POST'])
def registration():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SingUPForm()
    if form.validate_on_submit():
        password_hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=password_hashed)
        db.session.add(user)
        db.session.commit()
        flash(f'Your acount is create sucessfullly! you can login know!', 'success')
        return redirect(url_for('login'))
    
    return render_template('registration.html',
                           title='registration Page',
                           form = form)

@app.route('/login' , methods=['GET','POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        password = bcrypt.check_password_hash(user.password, form.password.data)
        if user and password:
            login_user(user=user, remember=form.remember.data)
            # this next is atribute, if it was in the url it mean that the user want to access to the account page
            # and so, if he login in this path, he will regirat this path account
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login uncuccessful! Please check your email and password', 'danger')
    return render_template('login.html',
                           title='LogIn Page',
                           form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


def UploadPicture(form_picture):
    random_fn = secrets.token_hex(8)
    _, fn_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_fn + fn_ext
    picture_path = os.path.join(app.root_path, 'static/Itemes', picture_fn)

    output_size = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)
    return picture_fn

@app.route('/account' , methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture_profile.data:
            picture_profile = UploadPicture(form.picture_profile.data)
            current_user.image_file = picture_profile
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been apdating successful!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'Itemes/{current_user.image_file}')
    print(f'Itemes/{current_user.image_file}')
    return render_template('account.html',
                           title='Account Page',
                           image_file=image_file,
                           form = form)



@app.route('/post/new' , methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('creat_post.html', 
                           title ='New Post',
                           form=form,
                           legend='New Post')


@app.route('/post/<user_id>')
def post(user_id):
    post = Post.query.get_or_404(user_id)
    return render_template('post.html', 
                           title ='Post',
                           post=post)


@app.route('/post/<int:user_id>/update' , methods=['GET','POST'])
@login_required
def update_post(user_id):
    post = Post.query.get_or_404(user_id)
    if current_user != post.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been Update!', 'success')
        return redirect(url_for('post', user_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('creat_post.html', 
                           title ='Update Post',
                           form = form,
                           legend='Update Post')