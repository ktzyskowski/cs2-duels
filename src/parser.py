import os

import pandas as pd
from demoparser2 import DemoParser


class DuelsParser:
    def __init__(self, window_length: int, window_lag: int = 0):
        self.window_length = window_length
        self.window_lag = window_lag
        self.attacker_dfs = []
        self.defender_dfs = []
        self.labels = []

    def __len__(self):
        return len(self.labels)

    def accumulate(self, path: str):
        parser = DemoParser(path)

        ticks = self.query_ticks(parser)
        map_name = self.query_map_name(parser)

        for death in self.query_player_deaths(parser).itertuples():
            # skip assisted kills
            if death.assister_steamid is not None:
                continue
            # attacker can be None when player gets hurt by c4 etc
            if (killer_id := death.attacker_steamid) is None:
                continue

            # filter down to ticks just before player death
            start, end = death.tick - self.window_length - self.window_lag, death.tick - self.window_lag
            event_df = ticks[ticks["tick"].between(start, end, inclusive="left")]

            # only include relevant player data (killer and victim)
            victim_id = death.user_steamid
            event_df = event_df[event_df["steamid"].isin([int(killer_id), int(victim_id)])]

            # skip if we do not have enough tick data to fill an event dataframe
            if len(event_df) != 2 * self.window_length:
                continue

            attacker_df = event_df[event_df["team_num"] == 2]  # 2 = t/attacker
            defender_df = event_df[event_df["team_num"] == 3]  # 3 = ct/defender
            idx = len(self)
            attacker_df.insert(0, "map_name", map_name)
            defender_df.insert(0, "map_name", map_name)
            attacker_df.insert(0, "index", idx)
            defender_df.insert(0, "index", idx)

            # 1 = attacker won, 0 = defender won
            label = 1 if death.attacker_name == attacker_df["name"].iloc[0] else 0

            self.attacker_dfs.append(attacker_df)
            self.defender_dfs.append(defender_df)
            self.labels.append(label)

    def compile(self):
        # if we have no data, return empty dataframes/series
        if not self.labels:
            return pd.DataFrame(), pd.DataFrame(), pd.Series()

        attacker_df = self.compile_df(self.attacker_dfs)
        defender_df = self.compile_df(self.defender_dfs)
        labels = pd.Series(self.labels, name="labels")
        return attacker_df, defender_df, labels

    @staticmethod
    def compile_df(dfs):
        df = pd.concat(dfs).set_index(["index", "tick"])
        df = df.drop(["name", "team_num", "steamid"], axis="columns")
        return df

    @staticmethod
    def query_map_name(parser: DemoParser):
        header = parser.parse_header()
        return header["map_name"]

    @staticmethod
    def query_player_deaths(parser: DemoParser):
        deaths = parser.parse_event("player_death", player=["team_name"], other=["is_warmup_period"])
        deaths = deaths[deaths["attacker_team_name"] != deaths["user_team_name"]]
        deaths = deaths[~deaths["is_warmup_period"]]
        return deaths

    @staticmethod
    def query_ticks(parser: DemoParser):
        wanted_props = [
            "team_num",  # filtering for attacker/defender

            # positional/spatial features
            # (potentially embed these with map_name?)
            "X",
            "Y",
            "Z",
            "pitch",  # pitch and yaw used together to create crosshair placement score
            "yaw",
            "velocity",  # most accurate when not moving! key feature of counterstrike

            # numeric features
            "health",  # higher -> better
            "armor_value",  # higher -> better
            "current_equip_value",  # proxy for weapon quality (instead of one-hotting "active_weapon_name")
            "balance",  # may indicate tendency to save/go aggro
            "flash_duration",  # how much time left while flashed?

            # boolean values
            # "in_crouch",  # more accurate but easier target
            "is_airborne",  # vulnerable while in-air, and makes noise after fall
            "is_scoped",  # high-risk high-reward with scoped weapons
            "is_walking",  # less noise made, but easier target
            "is_defusing",  # puts players in vulnerable state

            # game state
            "is_bomb_planted",  # flips role of attackers vs defenders
        ]
        ticks = parser.parse_ticks(wanted_props=wanted_props)
        return ticks


def parse_res(path: str, window_length: int = 128, window_lag: int = 0):
    duels_parser = DuelsParser(window_length=window_length, window_lag=window_lag)
    for filename in os.listdir(path):
        if not filename.endswith(".dem"):
            continue
        filepath = os.path.join(path, filename)
        duels_parser.accumulate(filepath)
    attacker_df, defender_df, labels = duels_parser.compile()
    return attacker_df, defender_df, labels
