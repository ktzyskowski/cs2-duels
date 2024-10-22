import math

import numpy as np


def aim_vector(pitch, yaw):
    cos_pitch = np.cos(pitch)
    return np.c_[
        np.cos(yaw) * cos_pitch,
        np.sin(yaw) * cos_pitch,
        -np.sin(pitch)
    ]


def crosshair_placement_score(attacker_df, defender_df):
    # convert pitch/yaw to radians
    attacker_pitch_rad = attacker_df["pitch"].values * math.pi / 180
    defender_pitch_rad = defender_df["pitch"].values * math.pi / 180
    attacker_yaw_rad = attacker_df["yaw"].values * math.pi / 180
    defender_yaw_rad = defender_df["yaw"].values * math.pi / 180

    # compute actual and theoretical "perfect" aim vectors
    attacker_aim = aim_vector(attacker_pitch_rad, attacker_yaw_rad)
    defender_aim = aim_vector(defender_pitch_rad, defender_yaw_rad)
    attacker_perfect_aim = defender_df[["X", "Y", "Z"]].values - attacker_df[["X", "Y", "Z"]].values
    defender_perfect_aim = attacker_df[["X", "Y", "Z"]].values - defender_df[["X", "Y", "Z"]].values

    # cosine similarity gets us crosshair placement score
    attacker_cps = (
            np.sum(attacker_aim * attacker_perfect_aim, axis=1)
            / (np.linalg.norm(attacker_aim, axis=1) * np.linalg.norm(attacker_perfect_aim, axis=1))
    )
    defender_cps = (
            np.sum(defender_aim * defender_perfect_aim, axis=1)
            / (np.linalg.norm(defender_aim, axis=1) * np.linalg.norm(defender_perfect_aim, axis=1))
    )
    return attacker_cps, defender_cps
