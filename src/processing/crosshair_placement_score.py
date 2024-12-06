import numpy as np


def to_vector(pitch, yaw):
    cos_pitch = np.cos(pitch)
    return np.c_[
        np.cos(yaw) * cos_pitch,
        np.sin(yaw) * cos_pitch,
        -np.sin(pitch)
    ]


def crosshair_alignment_score(samples):
    pitch_attacker = np.deg2rad(samples["pitch_attacker"])
    pitch_defender = np.deg2rad(samples["pitch_defender"])
    yaw_attacker = np.deg2rad(samples["yaw_attacker"])
    yaw_defender = np.deg2rad(samples["yaw_defender"])

    attacker_aim_vector = to_vector(pitch_attacker, yaw_attacker)
    defender_aim_vector = to_vector(pitch_defender, yaw_defender)
    attacker_to_defender_vector = (
            samples[["X_defender", "Y_defender", "Z_defender"]].values -
            samples[["X_attacker", "Y_attacker", "Z_attacker"]].values
    )
    defender_to_attacker_vector = (
            samples[["X_attacker", "Y_attacker", "Z_attacker"]].values -
            samples[["X_defender", "Y_defender", "Z_defender"]].values
    )

    attacker_crosshair_alignment = (
            np.sum(attacker_aim_vector * attacker_to_defender_vector, axis=1)
            / (np.linalg.norm(attacker_aim_vector, axis=1) * np.linalg.norm(attacker_to_defender_vector, axis=1))
    )
    defender_crosshair_alignment = (
            np.sum(defender_aim_vector * defender_to_attacker_vector, axis=1)
            / (np.linalg.norm(defender_aim_vector, axis=1) * np.linalg.norm(defender_to_attacker_vector, axis=1))
    )
    return attacker_crosshair_alignment, defender_crosshair_alignment
