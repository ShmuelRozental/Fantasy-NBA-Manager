from flask import request, jsonify, Blueprint
from db import db
from models.player import Player
from models.team import FantasyTeam
from services.team_service import check_duplicate_players, validate_player_count, validate_positions

teams = Blueprint('teams', __name__)


@teams.route('/fantasy_teams', methods=['POST'])
def create_fantasy_team():
    data = request.get_json()
    team_name = data.get('team_name')
    player_ids = data.get('player_ids')

    players = Player.query.filter(Player.id.in_(player_ids)).all()

    existing_players = {player.id: player.playerName for player in players if player.fantasy_team_id is not None}

    if existing_players:
        return jsonify(
            {'error': f'Players already in another fantasy team: {", ".join(existing_players.values())}'}), 400

    if error_response := validate_player_count(player_ids):
        return jsonify(error_response), 400

    if error_response := validate_positions(player_ids):
        return jsonify(error_response), 400

    fantasy_team = FantasyTeam(team_name=team_name)
    db.session.add(fantasy_team)
    db.session.commit()

    for player in players:
        player.fantasy_team_id = fantasy_team.id
        db.session.add(player)

    db.session.commit()

    return jsonify({"message": "Fantasy team created successfully."}), 201
@teams.route('/<int:team_id>', methods=['PUT'])
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
        # Clear current players from the team
        for player in team.players:
            player.fantasy_team_id = None  # Remove fantasy team association

        # Update with new players
        for player_id in player_ids:
            player = Player.query.get(player_id)
            if player:
                player.fantasy_team_id = team.id
            else:
                return jsonify({'error': f'Player with ID {player_id} not found.'}), 404

        db.session.commit()  # Save changes
        return jsonify({'message': 'Team updated successfully.'}), 200

    return jsonify({'error': 'Team not found.'}), 404

@teams.route('/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    team = FantasyTeam.query.get(team_id)
    if not team:
        return jsonify({'error': ' team dos not exist'}), 404

    db.session.delete(team)
    db.session.commit()
    return jsonify({'message': 'team successfully deleted'}), 200

@teams.route('/<int:team_id>', methods=['GET'])
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


@teams.route('/compare', methods=['GET'])
def compare_teams():
    team_ids = request.args.getlist('team')


    if len(team_ids) < 2:
        return jsonify({'error': 'you need provide 2 teams'}), 400

    teams = FantasyTeam.query.filter(FantasyTeam.id.in_(team_ids)).all()

    if len(teams) != len(team_ids):
        return jsonify({'error': 'one or more teams dose not exist'}), 404


    team_stats = []
    for team in teams:
        total_points = sum(player.get_total_points() for player in team.players)
        total_two_percent = sum(player.get_two_percent() for player in team.players) / len(
            team.players) if team.players else 0
        total_three_percent = sum(player.get_three_percent() for player in team.players) / len(
            team.players)if team.players else 0
        total_atr = sum(player.get_atr() for player in team.players) / len(team.players)
        ppg_ratios = sum(player.get_ppg_ratio() for player in team.players) / len(team.players)

        team_stats.append({
            'team': team.team_name,
            'points': total_points,
            'twoPercent': total_two_percent,
            'threePercent': total_three_percent,
            'ATR': total_atr,
            'PPG Ratio': ppg_ratios
        })


    sorted_team_stats = sorted(team_stats, key=lambda x: x['PPG Ratio'], reverse=True)

    return jsonify(sorted_team_stats), 200