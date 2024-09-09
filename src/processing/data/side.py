from enum import Enum


class Side(Enum):
    """Represents the side (team) of the player.

    Can either be ``Side.ATTACKER`` or ``Side.DEFENDER``. Sides swap halfway through the game, after 12 rounds.
    """

    ATTACKER = "attacker"
    DEFENDER = "defender"

    @classmethod
    def from_str(cls, side: str):
        if side == "T":
            return cls.ATTACKER
        else:
            return cls.DEFENDER
