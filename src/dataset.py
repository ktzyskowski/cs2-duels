import numpy as np
from torch.utils.data import Dataset


class DuelsDataset(Dataset):
    def __init__(self, attacker_df, defender_df, labels):
        self.attacker_df = attacker_df
        self.defender_df = defender_df
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        attacker_values = self.attacker_df.loc[idx].values.astype(np.float32)
        defender_values = self.defender_df.loc[idx].values.astype(np.float32)
        return attacker_values, defender_values, self.labels[idx]
