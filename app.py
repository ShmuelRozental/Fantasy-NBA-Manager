from flask import Flask
from flask_migrate import Migrate
from db import db
from routes.teams import teams

from routes.players import players
from utils.data_loader import load_players_from_api

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/rozen/projects/python/tests/Fantasy NBA Manager/fantasyNBAManager/instance/fantasy_nba.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    return app

app = create_app()


with app.app_context():
    db.drop_all()
    db.create_all()

    seasons = (2024, 2023, 2022)
    for season in seasons:
        print(f"Loading data for season {season}")
        season_data = load_players_from_api(f'http://b8c40s8.143.198.70.30.sslip.io/api/PlayerDataTotals/query?season={season}&&pageSize=1000', season)


app.register_blueprint(players)
app.register_blueprint(teams)

if __name__ == '__main__':
    app.run(debug=True)
