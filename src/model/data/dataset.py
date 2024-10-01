import pandas as pd
import torch

from torch.utils.data import Dataset
from processing.features.zyskowski import ZyskowskiFeatureExtractor
from processing.process import process

from sklearn.preprocessing import LabelEncoder


class DuelDataset(Dataset):
    def __init__(self, features: list[dict], labels: list):
        if len(features) != len(labels):
            raise ValueError("Features and labels must have the same length")

        if len(features) < 1:
            raise ValueError("Features and labels must have at least one sample")

        self.__init_y(labels)
        self.__init_x(features)

    def __init_y(self, labels):
        self.label_encoder = LabelEncoder().fit(list(map(str, labels)))
        self.y = torch.tensor(self.label_encoder.transform(labels), dtype=torch.long)

    def __init_x(self, features):
        temporal_features = [self.filter_temporal(sample) for sample in features]
        self.x_temporal = torch.tensor(
            [[value for key, value in sample.items()] for sample in temporal_features],
            dtype=torch.float,
        )

        snapshot_features = [self.filter_snapshot(sample) for sample in features]
        self.x_snapshot = pd.DataFrame(snapshot_features)
        # TODO: don't hardcode str one-hot encoding as just these two keys
        str_keys = ["attacker_active_weapon", "defender_active_weapon"]
        self.x_snapshot = pd.concat(
            [
                pd.get_dummies(self.x_snapshot[str_keys]),
                self.x_snapshot.drop(str_keys, axis=1),
            ],
            axis=1,
        )
        self.x_snapshot = torch.tensor(
            self.x_snapshot.values.astype(int), dtype=torch.long
        )

    @staticmethod
    def filter_temporal(sample):
        return {key: value for key, value in sample.items() if isinstance(value, list)}

    @staticmethod
    def filter_snapshot(sample):
        return {
            key: value for key, value in sample.items() if not isinstance(value, list)
        }

    def __len__(self):
        return len(self.y)

    def __getitem__(self, index):
        return None, self.y[index]


if __name__ == "__main__":
    result = process(path="../../../res/json", extractor=ZyskowskiFeatureExtractor())
    dataset = DuelDataset(features=result[0], labels=result[1])
    print(dataset.x_temporal.shape)
    print(dataset.x_snapshot.shape)
    print(dataset.y.shape)
