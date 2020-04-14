# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# fernetkey for encrypt password
FERNET_KEY = "Mnrj41xg6tDWY9OO-oUbALOBls2Z6-z6UPteatT23F0="


# Secret for mariadb
SECRET_KEY = "secret"
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "pythonlogin"
