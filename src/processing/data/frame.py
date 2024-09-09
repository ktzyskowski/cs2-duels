import math

from processing.data.util import Vector3, degrees_to_radians


class Frame:
    """Represents a single frame in a round."""

    def __init__(self, raw):
        self.tick = raw["tick"]
        self.attackers = Team(raw["t"])
        self.defenders = Team(raw["ct"])

    def get_player(self, player_id: int):
        """Get frame information for a specific player.

        :param player_id: the player id.
        :return: the player frame.
        """
        for player in self.attackers.players:
            if player.id == player_id:
                return player
        for player in self.defenders.players:
            if player.id == player_id:
                return player
        raise ValueError("Player not found")


class Team:
    """Represents frame information for a team."""

    def __init__(self, raw):
        self.players = list(map(Player, raw["players"]))


class Player:
    """Represents frame information for a player."""

    def __init__(self, raw):
        self.id = raw["steamID"]
        self.position = Vector3(raw["x"], raw["y"], raw["z"])
        self.velocity = Vector3(raw["velocityX"], raw["velocityY"], raw["velocityZ"])
        self.view_x = raw["viewX"]
        self.view_y = raw["viewY"]
        self.hp = raw["hp"]
        self.armor = raw["armor"]
        self.active_weapon = raw["activeWeapon"].lower()
        self.is_blinded = raw["isBlinded"]
        self.is_airborne = raw["isAirborne"]
        self.is_ducking = raw["isDucking"]
        self.is_standing = raw["isStanding"]
        self.is_scoped = raw["isScoped"]
        self.is_walking = raw["isWalking"]
        self.equipment_value = raw["equipmentValue"]
        self.cash = raw["cash"]
        self.has_helmet = raw["hasHelmet"]

    def crosshair_placement_score(self, target_player):
        """Compute the crosshair placement score for this player aiming at a target player.

        The score is defined as the cosine similarity between their placement and perfect placement.

        A score of +1 indicates that their aim is directly in the center of the target player.
        A score of -1 indicates that their aim is directly opposite the center of the target player.

        :param target_player: the target player.
        :return: the crosshair placement score.
        """
        # TODO: replace 0 with proper z (height) calculations
        # create straight-line vector from this player to the target player
        # (this represents PERFECT crosshair placement, since they're aiming directly at the target)
        perfect_placement = Vector3(
            target_player.position.x - self.position.x,
            target_player.position.y - self.position.y,
            0,
        )

        # now, calculate actual crosshair placement using view_x and view_y
        view_x_radians = degrees_to_radians(self.view_x)
        actual_placement = Vector3(
            math.cos(view_x_radians), math.sin(view_x_radians), 0
        )

        # score is the cosine similarity
        return perfect_placement.cosine_similarity(actual_placement)

    def distance(self, other_player):
        """Compute the straight-line distance between this player and another player.

        :param other_player: the other player.
        :return: the distance.
        """
        return self.position.distance(other_player.position)
