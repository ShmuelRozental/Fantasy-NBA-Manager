from models.player import Player

def process_player_data(players):
    result = []

    for player in players:
        seasons = [s.season for s in player.seasons]

        last_three_seasons = player.seasons[-3:]
        valid_two_percent = [s.twoPercent for s in last_three_seasons if s.twoPercent is not None]
        valid_three_percent = [s.threePercent for s in last_three_seasons if s.threePercent is not None]

        avg_two_percent = sum(valid_two_percent) / len(valid_two_percent) if valid_two_percent else 0
        avg_three_percent = sum(valid_three_percent) / len(valid_three_percent) if valid_three_percent else 0

        total_games = sum(s.games for s in player.seasons if s.games is not None)
        total_points = sum(s.points for s in player.seasons if s.points is not None)

        player_data = {
            'playerName': player.playerName,
            'team': player.team,
            'position': player.position,
            'seasons': seasons,
            'points': total_points,
            'games': total_games,
            'twoPercent': avg_two_percent,
            'threePercent': avg_three_percent,
        }

        for season_stats in player.seasons:
            player_data[season_stats.season] = {
                'ATR': season_stats.atr,
                'PPG_Ratio': season_stats.ppg_ratio,
            }

        result.append(player_data)

    return result