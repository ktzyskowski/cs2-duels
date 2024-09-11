from src.processing.data.util import Vector3


class Frame:
    """Represents a single frame in a round."""

    def __init__(self, raw):
        self.tick = raw["tick"]
        self.attackers = TeamFrame(raw["t"])
        self.defenders = TeamFrame(raw["ct"])

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


class TeamFrame:
    """Represents frame information for a team."""

    def __init__(self, raw):
        self.players = list(map(PlayerFrame, raw["players"]))


class PlayerFrame:
    """Represents frame information for a player."""

    def __init__(self, raw):
        self.id = raw["steamID"]
        self.position = Vector3(raw["x"], raw["y"], raw["z"])
        self.velocity = Vector3(raw["velocityX"], raw["velocityY"], raw["velocityZ"])
        self.view_x = raw["viewX"]  # both values stored in degrees [0, 360)
        self.view_y = raw["viewY"]  # convert to radians if needed
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
