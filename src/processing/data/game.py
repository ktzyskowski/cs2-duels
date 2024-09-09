import math
from collections import deque
from enum import Enum

from processing.data.util import sliding_window, Vector3, degrees_to_radians


class Side(Enum):
    """Represents the side (team) of the player.

    Can either be ``Side.ATTACKER`` or ``Side.DEFENDER``. Note that sides swap halfway through the game.
    """

    ATTACKER = "attacker"
    DEFENDER = "defender"

    @classmethod
    def from_str(cls, side: str):
        if side == "T":
            return cls.ATTACKER
        else:
            return cls.DEFENDER


class Game:
    """Represents a single game (map) played."""

    def __init__(self, raw):
        self.map = raw["mapName"]
        self.parse_rate = raw["parserParameters"]["parseRate"]
        self.rounds = list(map(Round, raw["gameRounds"]))
        self.kills = None
        self.deaths = None

    def iterate_kills_with_windows(self, window_size=4, clean=True):
        for r in self.rounds:
            yield from r.iterate_kills_with_windows(
                self.parse_rate, window_size=window_size, clean=clean
            )

    def _init_stat_counts(self):
        return {
            player_id: [0] * len(self.rounds)
            for player_id in self.rounds[0].attacker_ids
        } | {
            player_id: [0] * len(self.rounds)
            for player_id in self.rounds[0].defender_ids
        }

    def kills_by_round(self):
        if not self.kills:
            self.kills = self._init_stat_counts()
            for r in self.rounds:
                for k in r.kills:
                    if k.is_suicide or k.is_teamkill:
                        continue
                    self.kills[k.killer_id][k.game_round] += 1
        return self.kills

    def deaths_by_round(self):
        if not self.deaths:
            self.deaths = self._init_stat_counts()
            for r in self.rounds:
                for k in r.kills:
                    self.deaths[k.victim_id][k.game_round] += 1
        return self.deaths


class Round:
    """Represents a single round in a game."""

    def __init__(self, raw):
        self.kills = [Kill(kill_raw, raw["roundNum"]) for kill_raw in raw["kills"]]
        self.frames = list(map(Frame, raw["frames"]))
        self.attacker_ids = list(
            map(lambda player_raw: player_raw["steamID"], raw["tSide"]["players"])
        )
        self.defender_ids = list(
            map(lambda player_raw: player_raw["steamID"], raw["ctSide"]["players"])
        )

    def iterate_kills_with_windows(
        self, parse_rate: int, window_size: int, clean: bool
    ):
        """

        :param parse_rate:
        :param window_size:
        :param clean:
        :return:
        """
        # if no kills occurred in the round for whatever reason, return an empty iterable
        if not self.kills:
            return []

        # otherwise, create a stack of the kills (pop earliest first)
        # and generate sliding windows over frames in the round
        windows = sliding_window(self.frames, size=window_size)
        if clean:
            uniterated_kills = deque(k for k in self.kills if k.is_clean())
        else:
            uniterated_kills = deque(self.kills)

        # uniterated_kills = deque(self.kills if not clean else [k for k in self.kills if k.is_clean()])

        # loop over windows and kills to align them
        uniterated_kill = uniterated_kills.popleft()
        for window in windows:
            # window must occur directly before kill occurs
            while 0 < uniterated_kill.tick - window[-1].tick < parse_rate:
                yield uniterated_kill, window
                if uniterated_kills:
                    uniterated_kill = uniterated_kills.popleft()
                else:
                    return


class Kill:
    """Represents a processed kill event."""

    def __init__(self, raw, game_round: int):
        self.game_round = game_round - 1  # rounds start at 1, change to start at 0
        self.tick = raw["tick"]

        self.killer_id = raw["attackerSteamID"]
        self.killer_side = Side.from_str(raw["attackerSide"])
        self.victim_id = raw["victimSteamID"]
        self.victim_side = Side.from_str(raw["victimSide"])

        self.assister_sid = raw["assisterSteamID"]
        self.is_suicide = raw["isSuicide"]
        self.is_teamkill = raw["isTeamkill"]
        self.is_trade = raw["isTrade"]

    def attacker_id(self):
        """Get the ID of the attacker in this kill."""
        if self.victim_side == Side.ATTACKER and self.killer_side == Side.ATTACKER:
            raise RuntimeError("Both parties are attackers (team kill?)")
        elif self.victim_side == Side.ATTACKER:
            return self.victim_id
        elif self.killer_side == Side.ATTACKER:
            return self.killer_id
        else:
            raise RuntimeError("Neither party are attackers (team kill?)")

    def defender_id(self):
        """Get the ID of the defender in this kill."""
        if self.victim_side == Side.DEFENDER and self.killer_side == Side.DEFENDER:
            raise RuntimeError("Both parties are defenders (team kill?)")
        elif self.victim_side == Side.DEFENDER:
            return self.victim_id
        elif self.killer_side == Side.DEFENDER:
            return self.killer_id
        else:
            raise RuntimeError("Neither party are defenders (team kill?)")

    def is_clean(self):
        """Check if this kill is "clean", i.e. not an accidental teamkill, suicide, or assisted."""
        return (
            not self.is_suicide
            and not self.is_teamkill
            and not self.is_trade
            and self.assister_sid is None
        )


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
