from flask import Blueprint, jsonify, request
from models.player import Player, SeasonStats
from services.player_service import process_player_data

players = Blueprint('players', __name__)


@players.route('/', methods=['GET'])
def get_players():
    position = request.args.get('position')
    season = request.args.get('season')

    if position and position not in ['C', 'PF', 'SF', 'SG', 'PG']:
        return jsonify({"error": "Invalid position. Must be one of C, PF, SF, SG, PG."}), 400

    query = Player.query

    if position:
        query = query.filter_by(position=position)

    if season:
        query = query.join(SeasonStats).filter(SeasonStats.season == season)

    players = query.all()

    result = process_player_data(players)

    return jsonify(result)
