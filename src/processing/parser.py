import json

from processing.utils import sliding_window


def filter_kills(kills_data: list[dict]) -> list[dict]:
    """Filter a list of kills to remove edge-case kills.

    Removes team kills, suicides, assists (we only want pure 1v1 duels), and trades.

    :param kills_data: unfiltered kill data.
    :return: filtered kill data.
    """
    filtered_kills = []
    for kill in kills_data:
        if kill["isTeamkill"] or kill["isSuicide"] or kill["isTrade"] or kill["assisterSteamID"] is not None:
            continue
        filtered_kills.append(kill)
    return filtered_kills


def filter_round(round_data: dict, history_length=5) -> list:
    """Filter down round data to only include relevant tick information that occurs directly before a duel.

    :param round_data: the unaltered round data.
    :param history_length: the number of prior ticks to include.
    :return: filtered round data.
    """
    parsed_round = []
    kills, frames = round_data["kills"], round_data["frames"]

    # filter out team kills, assists, suicides
    kills = filter_kills(kills)

    for window in sliding_window(frames, size=history_length + 1):
        last_tick, second_last_tick = window[-1]["tick"], window[-2]["tick"]
        if kills:
            while kills:
                if second_last_tick < kills[0]["tick"] <= last_tick:
                    parsed_round.append({
                        "kill": kills.pop(0),
                        "leading_frames": window[:-1]
                    })
                else:
                    break
        else:
            return parsed_round


def parse_json(path: str):
    with open(path, "r") as f:
        data = json.load(f)

    filtered_rounds = map(filter_round, data["gameRounds"])
    return filtered_rounds
