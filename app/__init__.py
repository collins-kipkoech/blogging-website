from config import config_options
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet,configure_uploads,IMAGES
from flask_mail import Mail
from flask_bcrypt import Bcrypt
mail = Mail()

db=SQLAlchemy()
migrate=Migrate()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
photos = UploadSet('photos',IMAGES)
bcrypt = Bcrypt()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_options[config_name]) #load configuration variables
    configure_uploads(app,photos)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    #register blueprint
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # from app.auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint,url_prefix='/auth')

    return app



