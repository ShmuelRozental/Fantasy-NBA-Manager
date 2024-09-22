from models.player import Player
from models.team import FantasyTeam


def validate_player_count(player_ids):
    if len(player_ids) < 5:
        return {"error": "At least 5 players are required."}
    return None

def validate_positions(player_ids):
    positions = {player.position for player in Player.query.filter(Player.id.in_(player_ids)).all()}
    if len(positions) < 5:
        return {"error": "Must have one player in each position."}
    return None

def check_duplicate_players(team_id, player_ids):
    team_players = FantasyTeam.query.get(team_id).players if team_id else []
    if any(player_id in [player.id for player in team_players] for player_id in player_ids):
        return {"error": "Player is already in another team."}
    return None
