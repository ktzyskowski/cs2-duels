import functools

import pandas as pd
from demoparser2 import DemoParser

from src.processing.crosshair_placement_score import crosshair_alignment_score


class DemoFileParser:
    def __init__(self, filepath):
        self.parser = DemoParser(filepath)

    def get_map(self):
        return self.parser.parse_header()["map_name"]

    def parse(self):
        player_death_df = self._parse_player_deaths()
        ticks = self._parse_ticks()

        # create samples per each event
        samples = player_death_df.apply(
            functools.partial(self._transform, ticks=ticks),
            axis="columns",
        )

        # add engineered features
        attacker_crosshair_alignment, defender_crosshair_alignment = crosshair_alignment_score(samples)
        samples["crosshair_alignment_attacker"] = attacker_crosshair_alignment
        samples["crosshair_alignment_defender"] = defender_crosshair_alignment
        return samples

    def _parse_player_deaths(self):
        player_death_df = self.parser.parse_event(
            "player_death",
            player=["team_num"],
            other=["is_warmup_period"]
        ).convert_dtypes()

        # filter matches.txt team kills, warmup period, assists, and grenade kills
        player_death_df = player_death_df[player_death_df["attacker_team_num"] != player_death_df["user_team_num"]]
        player_death_df = player_death_df[~player_death_df["is_warmup_period"]]
        player_death_df = player_death_df[player_death_df["assister_steamid"].isna()]
        player_death_df = player_death_df[player_death_df["hitgroup"] != "generic"]
        return player_death_df

    def _parse_ticks(self):
        props = [
            # position / velocity / aim / physical attributes
            "X", "Y", "Z",
            "velocity",  # "velocity_X", "velocity_Y", "velocity_Z", <- do we want these?
            "pitch", "yaw",
            "duck_amount",
            # health/armor
            "health", "armor_value", "has_helmet",
            # economy
            "balance",
            "current_equip_value",
            # debuffs
            "flash_duration",
            # game state
            "is_bomb_planted",
            "t_losing_streak", "ct_losing_streak",
        ]
        ticks = self.parser.parse_ticks(props).convert_dtypes()
        ticks = ticks.dropna().reset_index(drop=True)
        return ticks

    @staticmethod
    def _transform(death, ticks, window_lag=16, window_step=1, window_length=1):
        """Transform a player death event into a training sample window.

        TODO: THIS METHOD JUST RETURNS LAST ROW OF TRAINING WINDOW FOR SCOPE OF THIS RESEARCH
              WE ARE ONLY INTERESTED IN DIRECT MOMENT BEFORE A DUEL

        ``window_lag`` controls how far back the sample occurs before the player death occurs, and
        ``window_step`` and ``window_length`` can both be set together to control the size and
        granularity of the sample.

        :param death: the player death event, passed as a Pandas namedtuple.
        :param ticks:
        :param window_lag: the distance (in ticks) from the end of the window to the event.
                           0 indicates the window should observe right up until the death.
        :param window_step: the granularity at which ticks are observed within the window (i.e. every nth tick).
        :param window_length: the length of the window (in ticks).
        :return: the training sample, or None if the underlying data associated with the player death is malformed/missing.
        """
        # figure matches.txt who is the attacker and who is the defender, based off of killer and victim involved in player death
        # 1 is    spectator
        # 2 is  t/attacker
        # 3 is ct/defender
        killer_team = death.attacker_team_num
        victim_team = death.user_team_num
        if killer_team == 2 and victim_team == 3:
            attacker_id = death.attacker_steamid
            defender_id = death.user_steamid
        elif killer_team == 3 and victim_team == 2:
            attacker_id = death.user_steamid
            defender_id = death.attacker_steamid
        else:
            # poisoned data point?
            raise RuntimeError("invalid player death, maybe bad data cleaning")

        tick_upper_bound = death.tick - window_lag
        tick_lower_bound = death.tick - window_lag - window_length
        event_ticks = ticks[ticks["tick"].between(tick_lower_bound, tick_upper_bound, inclusive="left")]

        # get attacker ticks
        attacker_ticks = event_ticks[event_ticks["steamid"] == int(attacker_id)]
        defender_ticks = event_ticks[event_ticks["steamid"] == int(defender_id)]
        if len(attacker_ticks) != window_length or len(defender_ticks) != window_length:
            # this means that we are missing some tick data, so throw away this sample
            print("throwaway sample!")
            return None

        # apply granularity controls
        attacker_ticks = attacker_ticks[::window_step].reset_index(drop=True)
        defender_ticks = defender_ticks[::window_step].reset_index(drop=True)

        # concatenate and return sample
        sample = pd.concat([attacker_ticks.add_suffix("_attacker"), defender_ticks.add_suffix("_defender")], axis=1)
        sample["attacker_won"] = True if killer_team == 2 else False

        # fix side-agnostic variables
        sample = sample.rename({
            "tick_attacker": "tick",
            "is_bomb_planted_attacker": "is_bomb_planted",
            "ct_losing_streak_attacker": "losing_streak_defender",
            "t_losing_streak_attacker": "losing_streak_attacker",
        }, axis="columns")
        sample = sample.drop(
            [
                "tick_defender",
                "is_bomb_planted_defender",
                "ct_losing_streak_defender",
                "t_losing_streak_defender",
            ],
            axis="columns"
        )
        return sample.iloc[-1]  # just return last row for this research


if __name__ == "__main__":
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    df = DemoFileParser("/Users/ktz/Downloads/faze-vs-mouz-m2-mirage-p1.dem").parse()
    print(df)
