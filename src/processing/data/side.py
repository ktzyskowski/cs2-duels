from enum import Enum


class Side(Enum):
    """Represents the side (team) of the player.

    Can either be ``Side.ATTACKER`` or ``Side.DEFENDER``. Sides swap halfway through the game, after 12 rounds. It is
    important to distinguish between attacker and defender when predicting duel outcomes, rather than treating either
    player as "player1" and "player2", because the rules of Counter Strike influence the decision-making of either
    party. For example, the attackers must push for control of the map in order to accomplish their objectives, leading
    to more aggressive plays for attackers than for defenders, who conversely must defend their territory.
    """

    ATTACKER = "attacker"
    DEFENDER = "defender"

    @classmethod
    def from_str(cls, side: str):
        if side == "T":
            return cls.ATTACKER
        elif side == "CT":
            return cls.DEFENDER
        raise ValueError(f"Unknown side: {side}")
