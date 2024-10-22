import numpy as np

from src.features.crosshair_placement_score import crosshair_placement_score
from src.parser import parse_res

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler


def main(res: str, window_length: int = 128):
    attacker_df, defender_df, labels = parse_res(res, window_length=window_length)

    # TODO: drop strings for now, figure out how to one-hot encode later
    # attacker_df = attacker_df.drop(["active_weapon_name"], axis="columns")
    # defender_df = defender_df.drop(["active_weapon_name"], axis="columns")
    attacker_df = attacker_df.drop(["map_name"], axis="columns")
    defender_df = defender_df.drop(["map_name"], axis="columns")

    # interpolate and back-fill missing values
    attacker_df = attacker_df.groupby("index").apply(
        lambda df: df.interpolate().bfill()
    ).reset_index(level=0, drop=True)
    defender_df = defender_df.groupby("index").apply(
        lambda df: df.interpolate().bfill()
    ).reset_index(level=0, drop=True)

    # normalize health and armor to [0, 1] range
    # attacker_df["health"] /= 100
    # defender_df["health"] /= 100
    # attacker_df["armor_value"] /= 100
    # defender_df["armor_value"] /= 100

    # compute crosshair placement scores
    attacker_cps, defender_cps = crosshair_placement_score(attacker_df, defender_df)
    attacker_df["cps"] = attacker_cps
    defender_df["cps"] = defender_cps

    # train/test split
    train_idx, test_idx = train_test_split(attacker_df.index.levels[0], test_size=0.2, random_state=42)
    attacker_train, attacker_test = attacker_df.loc[train_idx], attacker_df.loc[test_idx]
    defender_train, defender_test = defender_df.loc[train_idx], defender_df.loc[test_idx]
    y_train, y_test = labels[train_idx], labels[test_idx]

    # reshape dataframe objects to multidimensional numpy arrays
    num_features = attacker_train.shape[1]
    attacker_train = attacker_train.values.reshape(-1, window_length, num_features)
    attacker_test = attacker_test.values.reshape(-1, window_length, num_features)
    defender_train = defender_train.values.reshape(-1, window_length, num_features)
    defender_test = defender_test.values.reshape(-1, window_length, num_features)

    # make a preset conv kernel to squeeze temporal data
    # prioritize most recent tick information
    convolution_kernel = np.square(np.arange(window_length)).astype(float)
    convolution_kernel /= np.sum(convolution_kernel)
    attacker_train = np.sum(attacker_train * convolution_kernel[:, np.newaxis], axis=1)
    attacker_test = np.sum(attacker_test * convolution_kernel[:, np.newaxis], axis=1)
    defender_train = np.sum(defender_train * convolution_kernel[:, np.newaxis], axis=1)
    defender_test = np.sum(defender_test * convolution_kernel[:, np.newaxis], axis=1)

    # combine attacker defender into X variable
    x_train = np.concatenate([attacker_train, defender_train], axis=1)
    x_test = np.concatenate([attacker_test, defender_test], axis=1)

    # scale data
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    # fit logreg model
    model = LogisticRegression()
    model.fit(x_train, y_train)

    # compute metrics
    y_hat_train = model.predict(x_train)
    y_hat_test = model.predict(x_test)

    print("train accuracy", accuracy_score(y_train, y_hat_train))
    print("test accuracy", accuracy_score(y_test, y_hat_test))


if __name__ == "__main__":
    main("../../res/dem")
