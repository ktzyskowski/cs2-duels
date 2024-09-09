from typing import Callable

from processing.data.game import Kill, Frame, Player, Side


def iterate_player_frames(kill: Kill, window: list[Frame], side: Side):
    """Given a kill and window of leading frames, iterate through the frames of the players involved in the kill.

    :param kill: the kill.
    :param window: the frames leading up to the kill.
    :param side: the side of the player involved in the kill whose frames we want to iterate over.
    :return: a generator over the player frames.
    """
    if side == Side.ATTACKER:
        for frame in window:
            yield frame.get_player(kill.attacker_id())
    else:
        for frame in window:
            yield frame.get_player(kill.defender_id())


def extract_lambda(
    kill: Kill, window: list[Frame], func: Callable[[Player], object], name: str
):
    """Extract features from the given kill and player frames using a lambda function.

    :param kill: the kill.
    :param window: the frames leading up to the kill.
    :param func: the feature extractor.
    :param name: the name of the feature.
    :return: a dictionary containing the extracted features.
    """
    return {
        f"attacker_{name}": [
            func(p) for p in iterate_player_frames(kill, window, Side.ATTACKER)
        ],
        f"defender_{name}": [
            func(p) for p in iterate_player_frames(kill, window, Side.DEFENDER)
        ],
    }
