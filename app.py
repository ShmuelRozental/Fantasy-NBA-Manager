from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fantasy_nba.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)







if __name__ == '__main__':
    app.run()
