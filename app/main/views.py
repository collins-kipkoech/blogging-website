from flask import render_template,url_for, flash,redirect, request
from app import db,bcrypt
from . import main
from .forms import RegistrationForm, LoginForm, UpdateProfileForm, PostForm, UpdatePostForm
from app.models import User, Post,Comment
from flask_login import current_user, login_user, logout_user,login_required
from ..email import mail_message




@main.route('/')
def index():
    posts = Post.query.order_by(Post.date_posted.desc())
    title = 'Blogging Website'
    comments=Comment.query.all()
    return render_template('index.html',posts=posts,title=title,comments=comments)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('.index'))
    form = RegistrationForm()
    
    if form.validate_on_submit():
        
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        mail_message("Welcome to PicthesHub","email/welcome_user",user.email,user=user)

        return redirect(url_for('.login'))
    return render_template("register.html", title='Register', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Sign In', form=form)
@main.route('/logout')
def logout():
    """
    function to logout the user and redirects to the homepage
    """
    logout_user()
    return redirect(url_for('.index')) 




@main.route('/profile', methods=['GET','POST'])
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
    posts=Post.query.filter_by(user_id=current_user.id)
    comments=Comment.query.all()
        
    
    return render_template('profile.html',title='Edit Profile',form=form,posts=posts,comments=comments)





@main.route('/post',methods=['GET','POST'])
@login_required
def view_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully','success')
        return redirect(url_for('.index'))
    return render_template('post.html',form=form)


@main.route('/update_post', methods=['GET','POST'])
@login_required
def update_post():
    """
    function to update existing post
    """
    form = UpdatePostForm()
    if form.validate_on_submit():
        current_user.title = form.title.data        
        current_user.content = form.content.data
        
        
        db.session.commit()
        flash('Your changes have been saved.','success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.title.data = current_user.title
        form.content.data = current_user.content
        
    
    return render_template('post.html',title='Edit Post',form=form)

@main.route('/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    post=Post.query.filter_by(id=id).first()
    comment=request.args.get('comment')
    if comment!=None:
        new_comment=Comment(text=comment,post=id)
        db.session.add(new_comment)
        db.session.commit()
    return redirect(url_for('.index'))


@main.route('/delete/<post_id>')
@login_required
def delete_post(post_id):
  post = Post.query.get(post_id)
  db.session.delete(post)
  db.session.commit()
  flash('Your post has been deleted','success')
  return redirect(url_for('.profile'))



