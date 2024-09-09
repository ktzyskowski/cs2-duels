from processing.data.game import Game, Kill, Frame
from processing.features.common import extract_lambda


def extract_features(game: Game):
    features = []
    labels = []

    for kill, window in game.iterate_kills_with_windows(window_size=5):
        labels.append(kill.victim_side)
        features.append(
            {
                **extract_lambda(kill, window, func=lambda p: p.hp, name="hp"),
                **extract_lambda(kill, window, func=lambda p: p.armor, name="armor"),
                **extract_lambda(
                    kill, window, func=lambda p: p.is_blinded, name="is_blinded"
                ),
                **extract_lambda(
                    kill, window, func=lambda p: p.is_airborne, name="is_airborne"
                ),
                **extract_lambda(
                    kill, window, func=lambda p: p.is_ducking, name="is_ducking"
                ),
                **extract_lambda(
                    kill, window, func=lambda p: p.is_standing, name="is_standing"
                ),
                **extract_lambda(
                    kill, window, func=lambda p: p.is_scoped, name="is_scoped"
                ),
                **extract_lambda(
                    kill, window, func=lambda p: p.is_walking, name="is_walking"
                ),
                **extract_lambda(
                    kill,
                    window,
                    func=lambda p: p.equipment_value,
                    name="equipment_value",
                ),
                **extract_lambda(kill, window, func=lambda p: p.cash, name="cash"),
                **extract_lambda(
                    kill, window, func=lambda p: p.has_helmet, name="has_helmet"
                ),
                **extract_lambda(
                    kill, window, func=lambda p: p.active_weapon, name="active_weapon"
                ),
                **extract_total_hp(window),
                **extract_total_alive(window),
                **extract_team_equipment_value(window),
                **extract_kd_from_avg(kill, game),
            }
        )

        # left over features:

        # [ ] attacker_in_range_{200, 500, 1000, 2000}
        # [ ] defender_in_range_{200, 500, 1000, 2000}
        # adapt to attackers_in_range_of_attacker_{200, 500, 1000}
        # adapt to attackers_in_range_of_defender_{200, 500, 1000}
        # adapt to defenders_in_range_of_attacker_{200, 500, 1000}
        # adapt to defenders_in_range_of_defender_{200, 500, 1000}

        # [ ] enemy_hp_in_range_{500, 100, 2000}

    return features, labels


def extract_total_hp(window: list[Frame]):
    return {
        "attackers_hp": [
            sum(p.hp for p in frame.attackers.players) for frame in window
        ],
        "defenders_hp": [
            sum(p.hp for p in frame.defenders.players) for frame in window
        ],
    }


def extract_total_alive(window: list[Frame]):
    return {
        "attackers_alive": [
            len([p for p in frame.attackers.players if p.hp > 0]) for frame in window
        ],
        "defenders_alive": [
            len([p for p in frame.defenders.players if p.hp > 0]) for frame in window
        ],
    }


def extract_team_equipment_value(window: list[Frame]):
    return {
        "attackers_equipment_value": [
            sum(p.equipment_value for p in frame.attackers.players) for frame in window
        ],
        "defenders_equipment_value": [
            sum(p.equipment_value for p in frame.defenders.players) for frame in window
        ],
    }


def extract_kd_from_avg(kill: Kill, game: Game):
    kills, deaths = game.kills_by_round(), game.deaths_by_round()
    kills_avg = (
        sum(sum(kills[player_id][: kill.game_round]) for player_id in kills.keys()) / 10
    )
    deaths_avg = (
        sum(sum(deaths[player_id][: kill.game_round]) for player_id in kills.keys())
        / 10
    )
    return {
        "attacker_kills_from_avg": sum(kills[kill.attacker_id()][: kill.game_round])
        - kills_avg,
        "defender_kills_from_avg": sum(kills[kill.defender_id()][: kill.game_round])
        - kills_avg,
        "attacker_deaths_from_avg": sum(kills[kill.attacker_id()][: kill.game_round])
        - deaths_avg,
        "defender_deaths_from_avg": sum(kills[kill.defender_id()][: kill.game_round])
        - deaths_avg,
    }
