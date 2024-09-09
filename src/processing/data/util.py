import math
from dataclasses import dataclass
from math import sqrt


def sliding_window(lst: list, size: int):
    """Generate a sliding window over a list.

    :param lst: the data.
    :param size: the window size.
    :return: a generator of sliding windows.
    """
    for idx in range(len(lst) - size + 1):
        yield lst[idx : idx + size]


def degrees_to_radians(angle: float) -> float:
    """Convert the given angle from degrees to radians.

    :param angle: the angle in degrees.
    :return: the angle in radians
    """
    return angle * math.pi / 180


@dataclass
class Vector3:
    """Represents a vector with three dimensions."""

    x: float
    y: float
    z: float

    def magnitude(self):
        """Compute the magnitude of this vector.

        :return: the magnitude.
        """
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        """Return a normalized copy of this vector.

        :return: the normalized copy.
        """
        magnitude = self.magnitude()
        return Vector3(
            self.x / magnitude,
            self.y / magnitude,
            self.z / magnitude,
        )

    def dot(self, other):
        """Compute the dot product of this vector and another vector.

        :param other: the other vector.
        :return: the dot product.
        """
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

    def cosine_similarity(self, other):
        """Compute the cosine similarity between this vector and another vector.

        :param other: the other vector.
        :return: the cosine similarity.
        """
        return self.dot(other) / (self.magnitude() * other.magnitude())

    def distance(self, other):
        """Compute the straight-line distance between this vector and another vector.

        :param other: the other vector.
        :return: the distance.
        """
        return sqrt(
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )
