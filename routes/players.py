from flask import Blueprint, jsonify, request
from models.player import Player, SeasonStats

players = Blueprint('players', __name__)

@players.route('/api/players', methods=['GET'])
def get_players():
    position = request.args.get('position')
    season = request.args.get('season')

    if position and position not in ['C', 'PF', 'SF', 'SG', 'PG']:
        return jsonify({"error": "Invalid position. Must be one of C, PF, SF, SG, PG."}), 400

    query = Player.query

    if position:
        query = query.filter_by(position=position)

    if season:
        query = query.filter(Player.seasons.any(SeasonStats.season == season))

    players_list = query.all()

    result = []
    for player in players_list:
        total_points = sum(season.points for season in player.seasons)
        total_games = sum(season.games for season in player.seasons)
        avg_two_percent = sum(season.twoPercent for season in player.seasons) / len(player.seasons) if player.seasons else 0
        avg_three_percent = sum(season.threePercent for season in player.seasons) / len(player.seasons) if player.seasons else 0

        result.append({
            'playerName': player.playerName,
            'team': player.team,
            'position': player.position,
            'seasons': [season.season for season in player.seasons],
            'points': total_points,
            'games': total_games,
            'twoPercent': avg_two_percent,
            'threePercent': avg_three_percent,
            'ATR': player.ATR,
            'PPG_Ratio': player.PPG_Ratio
        })

    return jsonify(result)