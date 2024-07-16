from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from pathlib import Path
from enum import Enum

class PathUtils(Enum):
    BASE_DIR = Path(__file__).parent
    UPLOAD_DIR = BASE_DIR / 'static' / 'fotos_posts'

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///comunidade.db'
app.config["SECRET_KEY"] = "983104142cd8280425b5159c6a189b17"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"

from projeto_pinterest import routes
