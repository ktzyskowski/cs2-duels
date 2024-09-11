import unittest

from src.processing.data.frame import PlayerFrame
from src.processing.features.zyskowski import crosshair_placement_score


def create_test_player(x, y, z, view_x, view_y):
    raw = {
        "steamID": "test_id",
        "x": x,
        "y": y,
        "z": z,
        "viewX": view_x,
        "viewY": view_y,
        "velocityX": 0,
        "velocityY": 0,
        "velocityZ": 0,
        "hp": 0,
        "armor": 0,
        "activeWeapon": "knife",
        "isBlinded": False,
        "isAirborne": False,
        "isDucking": False,
        "isStanding": False,
        "isScoped": False,
        "isWalking": False,
        "equipmentValue": 850,
        "cash": 150,
        "hasHelmet": True,
    }
    return PlayerFrame(raw)


class TestCrosshairPlacementScore(unittest.TestCase):

    def test_looking_up(self):
        player1 = create_test_player(0, 0, 0, 0, 90)
        player2 = create_test_player(0, 0, 100, 0, 0)
        self.assertAlmostEqual(
            crosshair_placement_score(player1, player2), 1, delta=0.001
        )

        player2 = create_test_player(0, 0, -100, 0, 0)
        self.assertAlmostEqual(
            crosshair_placement_score(player1, player2), -1, delta=0.001
        )

        player2 = create_test_player(0, 100, 0, 0, 0)
        self.assertAlmostEqual(
            crosshair_placement_score(player1, player2), 0, delta=0.001
        )

        player2 = create_test_player(100, 0, 0, 0, 0)
        self.assertAlmostEqual(
            crosshair_placement_score(player1, player2), 0, delta=0.001
        )

    def test_real_kill(self):
        player1 = create_test_player(
            1350.0888671875,
            1765.399658203125,
            -226.13888549804688,
            200.599365234375,
            0.384521484375,
        )
        player2 = create_test_player(
            552.7427368164062,
            1457.29638671875,
            -226.29098510742188,
            20.0775146484375,
            0.0604248046875,
        )
        self.assertGreaterEqual(crosshair_placement_score(player1, player2), 0.99)

        player1 = create_test_player(
            -472.1568298339844,
            -1050.7161865234375,
            -351.96875,
            310.792236328125,
            0.4669189453125,
        )
        player2 = create_test_player(
            -56.47972106933594,
            -1550.7244873046875,
            -355.7255859375,
            130.80322265625,
            359.912109375,
        )
        self.assertGreaterEqual(crosshair_placement_score(player1, player2), 0.99)


class TestZyskowskiFeatures(unittest.TestCase):
    pass
