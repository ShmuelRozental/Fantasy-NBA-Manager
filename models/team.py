from sqlalchemy import Column, Integer, String, ForeignKey
from db import db

class FantasyTeam(db.Model):
    __tablename__ = 'fantasy_teams'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String, nullable=False)

    players = db.relationship('Player', backref='fantasy_team', lazy=True)


