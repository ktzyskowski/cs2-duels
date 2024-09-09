from collections import deque
from enum import Enum
from math import sqrt

from processing.data.util import sliding_window


def generify_side(side: str):
    if side == "T":
        return Side.ATTACKER
    else:
        return Side.DEFENDER


class Side(Enum):
    ATTACKER = "attacker"
    DEFENDER = "defender"


class Game:
    def __init__(self, raw):
        self.map = raw["mapName"]
        self.parse_rate = raw["parserParameters"]["parseRate"]
        self.rounds = list(map(Round, raw["gameRounds"]))
        self.kills = None
        self.deaths = None

    def iterate_kills_with_windows(self, window_size=4, clean=True):
        for r in self.rounds:
            yield from r.iterate_kills_with_windows(self.parse_rate, window_size=window_size, clean=clean)

    def _init_stat_counts(self):
        return {player_id: [0] * len(self.rounds) for player_id in self.rounds[0].attacker_ids} | \
            {player_id: [0] * len(self.rounds) for player_id in self.rounds[0].defender_ids}

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
    def __init__(self, raw):
        self.kills = [Kill(kill_raw, raw["roundNum"]) for kill_raw in raw["kills"]]
        self.frames = list(map(Frame, raw["frames"]))
        self.attacker_ids = list(map(lambda player_raw: player_raw["steamID"], raw["tSide"]["players"]))
        self.defender_ids = list(map(lambda player_raw: player_raw["steamID"], raw["ctSide"]["players"]))

    def iterate_kills_with_windows(self, parse_rate: int, window_size: int, clean: bool):
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
    def __init__(self, raw, game_round: int):
        self.game_round = game_round - 1  # rounds start at 1, change to start at 0
        self.tick = raw["tick"]

        self.killer_id = raw["attackerSteamID"]
        self.killer_side = generify_side(raw["attackerSide"])
        self.victim_id = raw["victimSteamID"]
        self.victim_side = generify_side(raw["victimSide"])

        self.assister_sid = raw["assisterSteamID"]
        self.is_suicide = raw["isSuicide"]
        self.is_teamkill = raw["isTeamkill"]
        self.is_trade = raw["isTrade"]

    def attacker_id(self):
        if self.victim_side == Side.ATTACKER and self.killer_side == Side.ATTACKER:
            raise RuntimeError("Both parties are attackers (team kill?)")
        elif self.victim_side == Side.ATTACKER:
            return self.victim_id
        elif self.killer_side == Side.ATTACKER:
            return self.killer_id
        else:
            raise RuntimeError("Neither party are attackers (team kill?)")

    def defender_id(self):
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
        return not self.is_suicide \
            and not self.is_teamkill \
            and not self.is_trade \
            and self.assister_sid is None


class Frame:
    def __init__(self, raw):
        self.tick = raw["tick"]
        self.attackers = Team(raw["t"])
        self.defenders = Team(raw["ct"])

    def get_player(self, player_id: int, player_side: Side):
        if player_side == Side.ATTACKER:
            team = self.attackers
        else:
            team = self.defenders
        for player in team.players:
            if player.id == player_id:
                return player
        raise ValueError("Player not found")


class Team:
    def __init__(self, raw):
        self.players = list(map(Player, raw["players"]))


class Player:
    def __init__(self, raw):
        self.id = raw["steamID"]
        self.x = raw["x"]
        self.y = raw["y"]
        self.z = raw["z"]
        self.velocity_x = raw["velocityX"]
        self.velocity_y = raw["velocityY"]
        self.velocity_z = raw["velocityZ"]
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

    def distance(self, other_player):
        return sqrt(
            (self.x - other_player.x) ** 2
            + (self.y - other_player.y) ** 2
            + (self.z - other_player.z) ** 2
        )
