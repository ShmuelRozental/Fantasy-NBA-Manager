from flask import Flask
from flask_migrate import Migrate
from db import db
from routes.players import players
from utils.data_loader import load_players_from_api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fantasy_nba.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(players)

with app.app_context():
    seasons = [2024, 2023, 2022]
    for season in seasons:
        print(season)
        url = f"http://b8c40s8.143.198.70.30.sslip.io/api/PlayerDataTotals/query?season={season}&&pageSize=1000"
        data_per_year = load_players_from_api(url)
        print(data_per_year)

if __name__ == '__main__':
    app.run(debug=True)
