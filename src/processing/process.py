import json

from processing.data.game import Game
from processing.features.zyskowski import ZyskowskiFeatureExtractor


if __name__ == "__main__":
    path = "../../res/json/0a5040e7-f972-4e0d-b9bf-ee6dfbdf0342.json"
    with open(path, "r") as f:
        data = json.load(f)

    test_game = Game(data)
    output = ZyskowskiFeatureExtractor().extract(test_game)
    print("done!")
