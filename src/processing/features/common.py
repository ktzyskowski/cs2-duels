from abc import ABC, abstractmethod
from typing import Callable

from src.processing.data.frame import PlayerFrame, Frame
from src.processing.data.game import Kill, Game
from src.processing.data.side import Side


class FeatureExtractor(ABC):
    def extract(self, game: Game, window_size: int = 4, clean: bool = True):
        """Extract features from a game.

        :param game: the game to extract features from.
        :param window_size: the window size. Default is 4.
        :param clean: whether the kill windows should be "clean". Default is true.
        :return: a tuple containing (features, labels).
        """
        features, labels = [], []
        for kill, window in game.iterate_kills(window_size=window_size, clean=clean):
            feature, label = self.extract_from_kill_window(kill, window)
            features.append(feature)
            labels.append(label)
        return features, labels

    @abstractmethod
    def extract_from_kill_window(self, kill: Kill, window: list[Frame]):
        """Extract a single (feature, label) tuple from a kill window.

        :param kill: the kill event.
        :param window: the frame window.
        :return: the (feature, label) tuple.
        """
        pass


def filter_player_frames(kill: Kill, window: list[Frame], side: Side):
    """Filter through the player frames of the attacker/defender directly involved in a kill.

    :param kill: the kill.
    :param window: the frames leading up to the kill.
    :param side: the side of the player involved in the kill whose frames we want to iterate over.
    :return: a generator over the player frames.
    """
    player_id = kill.attacker_id if side == Side.ATTACKER else kill.defender_id
    for frame in window:
        yield frame.get_player(player_id)


def extract_lambda(
    kill: Kill,
    window: list[Frame],
    func: Callable[[PlayerFrame], object],
    name: str,
    last_only: bool = False,
):
    """Extract features from the given kill and player frames using a lambda function.

    :param kill: the kill.
    :param window: the frames leading up to the kill.
    :param func: the feature extractor.
    :param name: the name of the feature.
    :param last_only: whether to only retrieve the last frame. Default is false.
    :return: a dictionary containing the extracted features.
    """
    attacker_stat = [func(p) for p in filter_player_frames(kill, window, Side.ATTACKER)]
    defender_stat = [func(p) for p in filter_player_frames(kill, window, Side.DEFENDER)]
    if last_only:
        attacker_stat, defender_stat = attacker_stat[-1], defender_stat[-1]
    return {f"attacker_{name}": attacker_stat, f"defender_{name}": defender_stat}
