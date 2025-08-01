from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os 


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app():

    
    

    


    app = Flask(__name__)
    TEMPLATE_DIR=os.path.abspath("../templates")

    app._static_folder="../static"

    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:12345@localhost/mydatabase'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secretkey'
    
    

    db.init_app(app)
    login_manager.init_app(app)

    from .routes import main
    from .api_routes import api

    app.register_blueprint(main)
    app.register_blueprint(api)

    return app
