from models.player import Player

def process_player_data(players):
    result = []

    for player in players:
        seasons = [s.season for s in player.seasons]

        last_three_seasons = player.seasons[-3:]
        avg_two_percent = player.get_two_percent()
        avg_three_percent = player.get_three_percent()
        total_points = player.get_total_points()
        total_games = sum(s.games for s in player.seasons if s.games is not None)

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