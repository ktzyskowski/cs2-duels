from processing.data.game import Game
from processing.features.common import extract_lambda


def extract_features(game: Game):
    features, labels = [], []
    for kill, window in game.iterate_kills_with_windows(window_size=5):
        labels.append(kill.victim_side)
        features.append(
            {
                **extract_lambda(kill, window, func=lambda p: p.hp, name="hp"),
                **extract_lambda(kill, window, func=lambda p: p.armor, name="armor"),
                **extract_lambda(kill, window, func=lambda p: p.position.x, name="x"),
                **extract_lambda(kill, window, func=lambda p: p.position.y, name="y"),
                **extract_lambda(kill, window, func=lambda p: p.position.z, name="z"),
                **extract_lambda(kill, window, func=lambda p: p.velocity.x, name="vx"),
                **extract_lambda(kill, window, func=lambda p: p.velocity.y, name="vy"),
                **extract_lambda(kill, window, func=lambda p: p.velocity.z, name="vz"),
            }
        )
    return features, labels
