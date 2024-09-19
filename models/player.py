from db import db

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    playerName = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    team = db.Column(db.String, nullable=False)
    seasons = db.relationship('SeasonStats', backref='player', lazy=True)

    @property
    def ATR(self):
        total_assists = sum(season.assists for season in self.seasons)
        total_turnovers = sum(season.turnovers for season in self.seasons)
        return total_assists / total_turnovers if total_turnovers else 0

    @property
    def PPG_Ratio(self):
        player_ppg = sum(season.points for season in self.seasons) / sum(
            season.games for season in self.seasons) if self.seasons else 0
        position_players = Player.query.filter_by(position=self.position).all()
        position_avg_ppg = sum(
            (sum(season.points for season in player.seasons) / sum(
                season.games for season in player.seasons) if player.seasons else 0)
            for player in position_players
        ) / len(position_players) if position_players else 0
        return player_ppg / position_avg_ppg if position_avg_ppg else 0

class SeasonStats(db.Model):
    __tablename__ = 'season_stats'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    season = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    games = db.Column(db.Integer, nullable=False)
    twoPercent = db.Column(db.Float, nullable=False)
    threePercent = db.Column(db.Float, nullable=False)
    assists = db.Column(db.Integer, nullable=False)
    turnovers = db.Column(db.Integer, nullable=False)




