import os

import pandas as pd

from src.parser import DuelsParser

pd.options.display.width = 1200
pd.options.display.max_colwidth = 100
pd.options.display.max_columns = 100

if __name__ == "__main__":
    # read demos in
    demo_dir = "res/dem"
    duels_parser = DuelsParser(window_length=128)
    for file_name in os.listdir(demo_dir):
        if not file_name.endswith(".dem"):
            continue
        filepath = os.path.join(demo_dir, file_name)
        duels_parser.accumulate(filepath)
    attacker_df, defender_df, labels = duels_parser.compile()

    print(attacker_df["map_name"].unique())

    print(attacker_df.head())

#
#     # normalize health and armor to [0, 1] range
#     attacker_df["health"] /= 100
#     defender_df["health"] /= 100
#     attacker_df["armor_value"] /= 100
#     defender_df["armor_value"] /= 100
#
#     # compute crosshair placement scores
#     attacker_cps, defender_cps = crosshair_placement_score(attacker_df, defender_df)
#     attacker_df["cps"] = attacker_cps
#     defender_df["cps"] = defender_cps
#
#     # drop strings for now, figure out how to one-hot encode
#     attacker_df = attacker_df.drop(["active_weapon_name"], axis="columns")
#     defender_df = defender_df.drop(["active_weapon_name"], axis="columns")
#     attacker_df = attacker_df.drop(["map_name"], axis="columns")
#     defender_df = defender_df.drop(["map_name"], axis="columns")
#
#     dataset = DuelsDataset(attacker_df, defender_df, labels)
#     print(len(dataset))
#     #
#     # dataloader = DataLoader(dataset, batch_size=64, shuffle=True)
#     # for x1, x2, y in dataloader:
#     #     print(x1.shape, x2.shape, y.shape)
