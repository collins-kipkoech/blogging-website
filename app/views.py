from flask import render_template,url_for, flash,redirect
from app import app
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post


posts = [
    {
        'author':'collins',
        'title':'football',
        'content':'i love football',
        'date_posted':'nov 2020'
    },
    {
        'author':'kipkoech',
        'title':'coding',
        'content':'i love coding',
        'date_posted':'nov 2020'
    }
]


@app.route('/')
def index():
    title = 'Blogging Website'
    return render_template('index.html',posts=posts,title=title)


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    title = 'Registration form'
    if form.validate_on_submit():
        flash(f'Account Created successfully','success')
        return redirect(url_for('login'))
    return render_template('register.html',title=title,form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    title = 'Login Here'
    if form.validate_on_submit():
        if form.username.data == 'collins' and form.password.data == '123':
            flash('Login successfully','success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check your username and password','danger')
    return render_template('login.html',form=form,title=title)
