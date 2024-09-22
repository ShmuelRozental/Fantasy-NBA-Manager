import requests
from models.player import Player, SeasonStats
from db import db


def calculate_position_averages(data):
    position_averages = {}
    positions = {player.get('position') for player in data if player.get('position')}

    for position in positions:
        total_points = sum(player.get('points', 0) for player in data if player.get('position') == position)
        total_games = sum(player.get('games', 0) for player in data if player.get('position') == position)

        avg_points_per_game = total_points / total_games if total_games > 0 else 0
        position_averages[position] = avg_points_per_game

    return position_averages


def update_player_data(player_data, season, position_averages):
    player = Player.query.filter_by(playerName=player_data.get('playerName')).first()

    if not player:
        player = Player(
            playerName=player_data.get('playerName'),
            team=player_data.get('team'),
            position=player_data.get('position')
        )
        db.session.add(player)
        db.session.flush()

    season_data = SeasonStats.query.filter_by(player_id=player.id, season=season).first()

    if not season_data:
        season_data = SeasonStats(
            player_id=player.id,
            season=season,
            points=player_data.get('points'),
            games=player_data.get('games'),
            twoPercent=player_data.get('twoPercent'),
            threePercent=player_data.get('threePercent') or 0.0,
            assists=player_data.get('assists'),
            turnovers=player_data.get('turnovers')
        )
        db.session.add(season_data)

    season_data.atr = season_data.assists / season_data.turnovers if season_data.turnovers else 0

    avg_points_per_game = position_averages.get(player.position, 0)
    if season_data.games > 0:
        season_data.ppg_ratio = (
                                            season_data.points / season_data.games) / avg_points_per_game if avg_points_per_game else 0
    else:
        season_data.ppg_ratio = 0


def load_players_from_api(api_url, season):
    response = requests.get(api_url)
    response.raise_for_status()

    data = response.json()

    position_averages = calculate_position_averages(data)

    for player_data in data:
        update_player_data(player_data, season, position_averages)

    db.session.commit()
