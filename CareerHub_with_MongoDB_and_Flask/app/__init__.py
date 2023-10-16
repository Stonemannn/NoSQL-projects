from flask import Flask

# __name__ is the package name - 'app', for locating templates and static files
# if we were to use a different name, we would have to specify the template folder and static folder
# for example, app = Flask(__main__), this would set the root path to the directory of run-app.py
app = Flask(__name__)

from app import jobs