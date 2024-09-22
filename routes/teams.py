from flask import request, jsonify, Blueprint
from db import db
from models.player import Player
from models.team import FantasyTeam
from services.team_service import check_duplicate_players, validate_player_count, validate_positions

teams = Blueprint('teams', __name__)
@teams.route('/api/fantasy_teams', methods=['POST'])
def create_fantasy_team():
    data = request.get_json()
    team_name = data.get('team_name')
    player_ids = data.get('player_ids')

    if error_response := validate_player_count(player_ids):
        return jsonify(error_response), 400

    if error_response := validate_positions(player_ids):
        return jsonify(error_response), 400

    fantasy_team = FantasyTeam(team_name=team_name)
    db.session.add(fantasy_team)
    db.session.commit()

    for player_id in player_ids:
        player = Player.query.get(player_id)
        player.fantasy_team_id = fantasy_team.id

    db.session.commit()
    return jsonify({"message": "Fantasy team created successfully."}), 201

@teams.route('/api/teams/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    data = request.get_json()
    player_ids = data.get('player_ids', [])

    if error_response := validate_player_count(player_ids):
        return jsonify(error_response), 400

    if error_response := validate_positions(player_ids):
        return jsonify(error_response), 400

    if error_response := check_duplicate_players(team_id, player_ids):
        return jsonify(error_response), 400

    team = FantasyTeam.query.get(team_id)
    if team:
        # Update logic...
        return jsonify({'message': 'Team updated successfully.'}), 200
    return jsonify({'error': 'Team not found.'}), 404

@teams.route('/api/teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    team = FantasyTeam.query.get(team_id)
    if not team:
        return jsonify({'error': ' team dos not exist'}), 404

    db.session.delete(team)
    db.session.commit()
    return jsonify({'message': 'team successfully deleted'}), 200

@teams.route('/api/teams/<int:team_id>', methods=['GET'])
def get_team(team_id):
    team = FantasyTeam.query.get(team_id)
    if not team:
        return jsonify({'error': ' team dos not exist'}), 404

    players_data = []
    for player in team.players:
        player_stats = {
            'playerName': player.playerName,
            'team': player.team,
            'position': player.position,
            'points': player.get_total_points(),
            'games': player.get_total_games(),
            'twoPercent': player.get_two_percent(),
            'threePercent': player.get_three_percent(),
            'atr': player.get_atr(),
            'ppg_ratio': player.get_ppg_ratio(),
        }
        players_data.append(player_stats)

    response = {
        'team_name': team.team_name,
        'players': players_data,
    }
    return jsonify(response), 200
