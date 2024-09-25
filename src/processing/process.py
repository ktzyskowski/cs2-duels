import json
import os

from processing.data.game import Game
from processing.features.common import FeatureExtractor
from processing.features.zyskowski import ZyskowskiFeatureExtractor


def process(path: str, extractor: FeatureExtractor):
    features, labels = [], []

    filenames = os.listdir(path)
    for filename in filenames:
        with open(os.path.join(path, filename), "r") as f:
            data = json.load(f)
            game = Game(data)
            new_features, new_labels = extractor.extract(game)
            features.extend(new_features)
            labels.extend(new_labels)
    return features, labels


if __name__ == "__main__":
    process(path="../../res/json", extractor=ZyskowskiFeatureExtractor())
