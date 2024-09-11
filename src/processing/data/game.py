from collections import deque

from src.processing.data.frame import Frame
from src.processing.data.side import Side
from src.processing.data.util import sliding_window


class Game:
    """Represents a single game (map) played."""

    def __init__(self, raw):
        self.map = raw["mapName"]
        self.parse_rate = raw["parserParameters"]["parseRate"]
        self.rounds = list(map(Round, raw["gameRounds"]))
        self.kills = None
        self.deaths = None

    def iterate_kills(self, window_size: int, clean: bool):
        """Iterate over all the kills in this game, and include the window of frames leading up to each kill.

        :param window_size: the size of the window (number of frames prior to the kill).
        :param clean: whether to only include "clean" kills. I.E. no suicides, teamkills, trades, assists.
        :return: a generator over the kills and their respective windows.
        """
        for r in self.rounds:
            yield from r.iterate_kills(
                self.parse_rate, window_size=window_size, clean=clean
            )

    # def kills_by_round(self):
    #     """Get the number of kills for each player in the game, separated by round.
    #
    #     :return: a dictionary of the kills by round.
    #     """
    #     if not self.kills:
    #         self.kills = self._init_stat_counts()
    #         for r in self.rounds:
    #             for k in r.kills:
    #                 if k.is_suicide or k.is_teamkill:
    #                     continue
    #                 self.kills[k.killer_id][k.game_round] += 1
    #     return self.kills
    #
    # def deaths_by_round(self):
    #     """Get the number of deaths for each player in the game, separated by round.
    #
    #     :return: a dictionary of the deaths by round.
    #     """
    #     if not self.deaths:
    #         self.deaths = self._init_stat_counts()
    #         for r in self.rounds:
    #             for k in r.kills:
    #                 self.deaths[k.victim_id][k.game_round] += 1
    #     return self.deaths
    #
    # def _init_stat_counts(self):
    #     return {
    #         player_id: [0] * len(self.rounds)
    #         for player_id in self.rounds[0].attacker_ids
    #     } | {
    #         player_id: [0] * len(self.rounds)
    #         for player_id in self.rounds[0].defender_ids
    #     }


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

    def iterate_kills(self, parse_rate: int, window_size: int, clean: bool):
        """Iterate over all the kills in this round, and include the window of frames leading up to each kill.

        :param parse_rate: the parse rate of the underlying data. This helps determine which frames precede a kill.
        :param window_size: the size of the window (number of frames prior to the kill).
        :param clean: whether to only include "clean" kills. I.E. no suicides, teamkills, trades, assists.
        :return: a generator over the kills and their respective windows.
        """
        # if no kills occurred in the round for whatever reason, return an empty iterable
        if not self.kills:
            return []

        # otherwise, create a stack of the kills (pop earliest first)
        # and generate sliding windows over frames in the round
        windows = sliding_window(self.frames, size=window_size)
        if clean:
            uniterated_kills = deque(k for k in self.kills if k.is_clean)
        else:
            uniterated_kills = deque(self.kills)

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
        self.distance = raw["distance"]

        self.assister_id = raw["assisterSteamID"]
        self.is_suicide = raw["isSuicide"]
        self.is_teamkill = raw["isTeamkill"]
        self.is_trade = raw["isTrade"]

        if self.is_suicide:
            self.killer_id, self.killer_side, self.victim_id, self.victim_side = (
                None,
                None,
                None,
                None,
            )
        else:
            self.killer_id = raw["attackerSteamID"]
            self.victim_id = raw["victimSteamID"]
            self.killer_side = Side.from_str(raw["attackerSide"])
            self.victim_side = Side.from_str(raw["victimSide"])

    @property
    def attacker_id(self):
        """Get the ID of the attacker in this kill."""
        return self.by_side(
            Side.ATTACKER,
            if_victim=lambda: self.victim_id,
            if_killer=lambda: self.killer_id,
        )

    @property
    def defender_id(self):
        """Get the ID of the defender in this kill."""
        return self.by_side(
            Side.DEFENDER,
            if_victim=lambda: self.victim_id,
            if_killer=lambda: self.killer_id,
        )

    @property
    def is_clean(self):
        """Check if this kill is "clean", i.e. not an accidental teamkill, suicide, or assisted."""
        return (
            not self.is_suicide
            and not self.is_teamkill
            and not self.is_trade
            and self.assister_id is None
        )

    def by_side(self, side, if_victim, if_killer):
        if self.victim_side is side and self.killer_side is side:
            raise RuntimeError(f"Both parties are {side.value}s (team kill?)")
        elif self.victim_side is side:
            return if_victim()
        elif self.killer_side is side:
            return if_killer()
        else:
            raise RuntimeError(f"Neither party are {side.value}s (team kill?)")
