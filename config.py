import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Flask config
SECRET_KEY = 'elizardo_perez_secret_2024_cochabamba'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'escuela.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-AppBuilder config
APP_NAME = "U.E. Profesor Elizardo Pérez G."
APP_ICON = ""
APP_THEME = ""

FAB_API_SWAGGER_UI = True

# Auth
AUTH_TYPE = 1  # DB auth
AUTH_ROLE_ADMIN = 'Admin'
AUTH_ROLE_PUBLIC = 'Public'
AUTH_USER_REGISTRATION = False

# Babel
BABEL_DEFAULT_LOCALE = 'es'
BABEL_DEFAULT_FOLDER = 'translations'
LANGUAGES = {
    'es': {'flag': 'bo', 'name': 'Español'},
    'en': {'flag': 'us', 'name': 'English'},
}
