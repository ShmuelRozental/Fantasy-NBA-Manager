from sqlalchemy import Column, Integer, ForeignKey
from db import db

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playerName = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    team = db.Column(db.String, nullable=False)
    fantasy_team_id = db.Column(db.Integer, db.ForeignKey('fantasy_teams.id'), nullable=True)
    seasons = db.relationship('SeasonStats', backref='player', lazy=True)


    def get_total_points(self):
        return sum(season.points for season in self.seasons)


    def get_two_percent(self):
        total_two_percent = sum(season.twoPercent for season in self.seasons if season.twoPercent is not None)
        return total_two_percent / len(self.seasons) if self.seasons else 0


    def get_three_percent(self):
        total_three_percent = sum(season.threePercent for season in self.seasons if season.threePercent is not None)
        return total_three_percent / len(self.seasons) if self.seasons else 0


    def get_atr(self):
        total_atr = sum(season.atr for season in self.seasons if season.atr is not None)
        return total_atr / len(self.seasons) if self.seasons else 0


    def get_ppg_ratio(self):
        total_ppg_ratio = sum(season.ppg_ratio for season in self.seasons if season.ppg_ratio is not None)
        return total_ppg_ratio / len(self.seasons) if self.seasons else 0



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




