from flask import Flask
from  flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'AbCDefGHIjklmnOPqRsTuVwxyZ'

db = SQLAlchemy(app)


from blog import routes