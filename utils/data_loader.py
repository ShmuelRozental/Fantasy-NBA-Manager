import requests
from models.player import Player, SeasonStats
from db import db


def load_players_from_api(api_url):
    response = requests.get(api_url)
    data = response.json()


    print(f"Data received for URL {api_url}: {data}")

    for player_data in data:

        player = Player.query.get(player_data.get('id'))


        if not player:
            player = Player(
                id=player_data.get('id'),
                playerName=player_data.get('playerName'),
                team=player_data.get('team'),
                position=player_data.get('position')
            )
            db.session.add(player)


        season_data = SeasonStats.query.filter_by(player_id=player.id, season=player_data.get('season')).first()


        if not season_data:
            season_data = SeasonStats(
                player_id=player.id,
                season=player_data.get('season'),
                points=player_data.get('points'),
                games=player_data.get('games'),
                twoPercent=player_data.get('twoPercent'),
                threePercent=player_data.get('threePercent'),
                assists=player_data.get('assists'),
                turnovers=player_data.get('turnovers')
            )
            db.session.add(season_data)
        else:

            season_data.points = player_data.get('points')
            season_data.games = player_data.get('games')
            season_data.twoPercent = player_data.get('twoPercent')
            season_data.threePercent = player_data.get('threePercent')
            season_data.assists = player_data.get('assists')
            season_data.turnovers = player_data.get('turnovers')


    db.session.commit()
    return data