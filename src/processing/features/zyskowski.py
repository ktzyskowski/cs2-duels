import math

from src.processing.data.frame import Frame, PlayerFrame
from src.processing.data.game import Kill
from src.processing.data.util import Vector3, degrees_to_radians
from src.processing.features.common import extract_lambda, FeatureExtractor


class ZyskowskiFeatureExtractor(FeatureExtractor):
    def extract_from_kill_window(self, kill: Kill, window: list[Frame]):
        feature = {
            **extract_lambda(kill, window, func=lambda p: p.position.x, name="x"),
            **extract_lambda(kill, window, func=lambda p: p.position.y, name="y"),
            **extract_lambda(kill, window, func=lambda p: p.position.z, name="z"),
            **extract_lambda(kill, window, func=lambda p: p.velocity.x, name="vx"),
            **extract_lambda(kill, window, func=lambda p: p.velocity.y, name="vy"),
            **extract_lambda(kill, window, func=lambda p: p.velocity.z, name="vz"),
            **extract_lambda(
                kill, window, func=lambda p: p.hp, name="hp", last_only=True
            ),
            **extract_lambda(
                kill, window, func=lambda p: p.armor, name="armor", last_only=True
            ),
            **extract_lambda(
                kill,
                window,
                func=lambda p: p.is_blinded,
                name="is_blinded",
                last_only=True,
            ),
            **extract_lambda(
                kill,
                window,
                func=lambda p: p.is_airborne,
                name="is_airborne",
                last_only=True,
            ),
            **extract_lambda(
                kill,
                window,
                func=lambda p: p.is_ducking,
                name="is_ducking",
                last_only=True,
            ),
            **extract_lambda(
                kill,
                window,
                func=lambda p: p.is_standing,
                name="is_standing",
                last_only=True,
            ),
            **extract_lambda(
                kill,
                window,
                func=lambda p: p.is_scoped,
                name="is_scoped",
                last_only=True,
            ),
            **extract_lambda(
                kill,
                window,
                func=lambda p: p.is_walking,
                name="is_walking",
                last_only=True,
            ),
            **extract_lambda(
                kill,
                window,
                func=lambda p: p.equipment_value,
                name="equipment_value",
                last_only=True,
            ),
            **extract_lambda(
                kill, window, func=lambda p: p.cash, name="cash", last_only=True
            ),
            **extract_lambda(
                kill,
                window,
                func=lambda p: p.has_helmet,
                name="has_helmet",
                last_only=True,
            ),
            **extract_lambda(
                kill,
                window,
                func=lambda p: p.active_weapon,
                name="active_weapon",
                last_only=True,
            ),
            **extract_crosshair_placement_score(kill, window),
        }

        # label is the winner of the duel, either attacker or defender
        label = kill.killer_side
        return feature, label


def extract_crosshair_placement_score(kill: Kill, window: list[Frame]):
    feature = {
        "attacker_crosshair_placement_score": [],
        "defender_crosshair_placement_score": [],
    }
    for frame in window:
        attacker = frame.get_player(kill.attacker_id)
        defender = frame.get_player(kill.defender_id)
        feature["attacker_crosshair_placement_score"].append(
            crosshair_placement_score(attacker, defender)
        )
        feature["defender_crosshair_placement_score"].append(
            crosshair_placement_score(defender, attacker)
        )
    return feature


def crosshair_placement_score(player: PlayerFrame, target: PlayerFrame):
    """Compute the crosshair placement score for a player aiming at a target player.

    The score is defined as the cosine similarity between their placement and perfect placement.

    A score of +1 indicates that their aim is directly in the center of the target player.
    A score of -1 indicates that their aim is directly opposite the center of the target player.

    :param player: the player whose score we are calculating.
    :param target: the target player being aimed at.
    :return: the crosshair placement score.
    """
    # create straight-line vector from this player to the target player
    # (this represents PERFECT crosshair placement, since they're aiming directly at the target)
    perfect_placement = Vector3(
        target.position.x - player.position.x,
        target.position.y - player.position.y,
        target.position.z - player.position.z,
    )

    # now, calculate actual crosshair placement using view_x and view_y
    view_x_radians = degrees_to_radians(player.view_x)
    view_y_radians = degrees_to_radians(player.view_y)
    xz_length = math.cos(view_y_radians)
    actual_placement = Vector3(
        math.cos(view_x_radians) * xz_length,
        math.sin(view_x_radians) * xz_length,
        math.sin(view_y_radians),
    )

    # score is the cosine similarity
    return perfect_placement.cosine_similarity(actual_placement)


# def extract_total_hp(window: list[Frame]):
#     return {
#         "attackers_hp": [
#             sum(p.hp for p in frame.attackers.players) for frame in window
#         ],
#         "defenders_hp": [
#             sum(p.hp for p in frame.defenders.players) for frame in window
#         ],
#     }
#
#
# def extract_total_alive(window: list[Frame]):
#     return {
#         "attackers_alive": [
#             len([p for p in frame.attackers.players if p.hp > 0]) for frame in window
#         ],
#         "defenders_alive": [
#             len([p for p in frame.defenders.players if p.hp > 0]) for frame in window
#         ],
#     }
#
#
# def extract_team_equipment_value(window: list[Frame]):
#     return {
#         "attackers_equipment_value": [
#             sum(p.equipment_value for p in frame.attackers.players) for frame in window
#         ],
#         "defenders_equipment_value": [
#             sum(p.equipment_value for p in frame.defenders.players) for frame in window
#         ],
#     }
#
#
# def extract_kd_from_avg(kill: Kill, game: Game):
#     kills, deaths = game.kills_by_round(), game.deaths_by_round()
#     kills_avg = (
#         sum(sum(kills[player_id][: kill.game_round]) for player_id in kills.keys()) / 10
#     )
#     deaths_avg = (
#         sum(sum(deaths[player_id][: kill.game_round]) for player_id in kills.keys())
#         / 10
#     )
#     return {
#         "attacker_kills_from_avg": sum(kills[kill.attacker_id()][: kill.game_round])
#         - kills_avg,
#         "defender_kills_from_avg": sum(kills[kill.defender_id()][: kill.game_round])
#         - kills_avg,
#         "attacker_deaths_from_avg": sum(kills[kill.attacker_id()][: kill.game_round])
#         - deaths_avg,
#         "defender_deaths_from_avg": sum(kills[kill.defender_id()][: kill.game_round])
#         - deaths_avg,
#     }
