from sqlalchemy import Column, Integer, ForeignKey
from db import db

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playerName = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    team = db.Column(db.String, nullable=False)
    fantasy_team_id = db.Column(db.Integer, db.ForeignKey('fantasy_teams.id'))
    seasons = db.relationship('SeasonStats', backref='player', lazy=True)




class SeasonStats(db.Model):
    __tablename__ = 'season_stats'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    season = db.Column(db.String, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    games = db.Column(db.Integer, nullable=False)
    twoPercent = db.Column(db.Float, nullable=True)
    threePercent = db.Column(db.Float, nullable=True)
    assists = db.Column(db.Integer, nullable=False)
    turnovers = db.Column(db.Integer, nullable=False)
    ppg_ratio = db.Column(db.Float, nullable=True)
    atr = db.Column(db.Float, nullable=True)

