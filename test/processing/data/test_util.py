import math
import unittest

from src.processing.data.util import degrees_to_radians, sliding_window, Vector3


class TestUtilityFunctions(unittest.TestCase):
    def test_sliding_window(self):
        self.assertListEqual(
            list(sliding_window([1, 2, 3, 4, 5, 6, 7], size=3)),
            [
                [1, 2, 3],
                [2, 3, 4],
                [3, 4, 5],
                [4, 5, 6],
                [5, 6, 7],
            ],
        )

        self.assertListEqual(
            list(sliding_window([1, 2, 3, 4, 5, 6, 7], size=2)),
            [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]],
        )

    def test_degrees_to_radians(self):
        self.assertAlmostEqual(degrees_to_radians(90), math.pi / 2, delta=0.001)
        self.assertAlmostEqual(degrees_to_radians(180), math.pi, delta=0.001)


class TestVector3(unittest.TestCase):
    def test_magnitude(self):
        vec = Vector3(1, 2, 3)
        self.assertAlmostEqual(vec.magnitude(), math.sqrt(14), delta=0.001)

        vec = Vector3(1, -5, 3)
        self.assertAlmostEqual(vec.magnitude(), math.sqrt(35), delta=0.001)

    def test_normalize(self):
        vec = Vector3(1, 2, 3)
        vec_norm = vec.normalize()
        self.assertAlmostEqual(vec_norm.magnitude(), 1, delta=0.001)
        self.assertAlmostEqual(vec_norm.cosine_similarity(vec), 1, delta=0.001)

    def test_dot(self):
        vec1 = Vector3(1, 2, 3)
        vec2 = Vector3(5, -5, 4)
        self.assertAlmostEqual(vec1.dot(vec2), 7, delta=0.001)

    def test_cosine_similarity(self):
        vec1 = Vector3(1, 1, 1)
        vec2 = Vector3(-1, -1, -1)
        vec3 = Vector3(4, 4, 4)
        self.assertAlmostEqual(vec1.cosine_similarity(vec2), -1, delta=0.001)
        self.assertAlmostEqual(vec1.cosine_similarity(vec3), 1, delta=0.001)

        vec4 = Vector3(1, 2, 3)
        vec5 = Vector3(2, 4, 6)
        self.assertAlmostEqual(vec4.cosine_similarity(vec5), 1, delta=0.001)

        vec4 = Vector3(0, 0, 1)
        vec5 = Vector3(0, 1, 0)
        self.assertAlmostEqual(vec4.cosine_similarity(vec5), 0, delta=0.001)

    def test_distance(self):
        vec1 = Vector3(0, 0, 0)
        vec2 = Vector3(1, 2, 3)
        self.assertAlmostEqual(vec1.distance(vec2), math.sqrt(14), delta=0.001)
