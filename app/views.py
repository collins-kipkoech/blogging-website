from flask import render_template,url_for, flash,redirect, request
from app import app,db,bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateProfileForm, PostForm
from app.models import User, Post
from flask_login import current_user, login_user, logout_user,login_required




@app.route('/')
def index():
    posts = Post.query.all()
    title = 'Blogging Website'
    return render_template('index.html',posts=posts,title=title)


@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    title = 'Registration form'

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created successfully','success')
        return redirect(url_for('login'))
    return render_template('register.html',title=title,form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    title = 'Login Here'
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not bcrypt.check_password_hash(user.password,form.password.data):
            flash('Login unsuccessful. Please check your username and password','danger')
            return redirect(url_for('login'))
        else:
            login_user(user, remember=form.remember.data)
            flash('Login successfully','success')
        return redirect(url_for('index'))

        
    return render_template('login.html',form=form,title=title)

@app.route('/logout')
def logout():
    """
    function to logout the user and redirects to the homepage
    """
    logout_user()
    return redirect(url_for('index')) 




@app.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    """
    function to display and update user profile
    """
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data        
        current_user.email = form.email.data
        
        
        db.session.commit()
        flash('Your changes have been saved.','success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    
    return render_template('profile.html',title='Edit Profile',form=form)





@app.route('/post',methods=['GET','POST'])
@login_required
def view_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully','success')
        return redirect(url_for('index'))
    return render_template('post.html',form=form)


@pp.route('post1/int:post_id')
def post1(post_id):
    post = Post.query.get(post_id)
    return render_template('post1.html',post=post)


