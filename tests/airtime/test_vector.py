import unittest
import math
from airtime import Vector, dot, cross, norm, angle_between


class VectorTestCase(unittest.TestCase):
    def test_addition(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(4, 5, 6)
        result = v1 + v2
        self.assertEqual(result, Vector(5, 7, 9))

    def test_subtraction(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(4, 5, 6)
        result = v1 - v2
        self.assertEqual(result, Vector(-3, -3, -3))

    def test_multiplication(self):
        v = Vector(1, 2, 3)
        scalar = 2
        result = v * scalar
        self.assertEqual(result, Vector(2, 4, 6))

    def test_division(self):
        v = Vector(1, 2, 3)
        scalar = 2
        result = v / scalar
        self.assertEqual(result, Vector(0.5, 1, 1.5))

    def test_length(self):
        v = Vector(3, 4, 5)
        result = v.length()
        self.assertEqual(result, math.sqrt(50))

    def test_normalized(self):
        v = Vector(3, 4, 5)
        result = v.normalized()
        self.assertAlmostEqual(result.length(), 1.0)

    def test_dot_product(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(4, 5, 6)
        result = dot(v1, v2)
        self.assertEqual(result, 32)

    def test_cross_product(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(4, 5, 6)
        result = cross(v1, v2)
        self.assertEqual(result, Vector(-3, 6, -3))

    def test_norm(self):
        v = Vector(3, 4, 5)
        result = norm(v)
        self.assertEqual(result, math.sqrt(50))

    def test_angle_between(self):
        v1 = Vector(1, 0, 0)
        v2 = Vector(0, 1, 0)
        result = angle_between(v1, v2)
        self.assertAlmostEqual(result, math.pi / 2)

        v3 = Vector(1, 0, 0)
        v4 = Vector(1, 0, 0)
        result = angle_between(v3, v4)
        self.assertAlmostEqual(result, 0)

        v5 = Vector(1, 0, 0)
        v6 = Vector(-1, 0, 0)
        result = angle_between(v5, v6)
        self.assertAlmostEqual(result, math.pi)

    def test_is_close(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(1, 2, 3)
        self.assertTrue(v1.isclose(v2))

        v3 = Vector(1, 2, 3)
        v4 = Vector(1.0000001, 2.0000001, 3.0000001)
        self.assertTrue(v3.isclose(v4))

        v5 = Vector(1, 2, 3)
        v6 = Vector(1.1, 2.1, 3.1)
        self.assertFalse(v5.isclose(v6))


if __name__ == "__main__":
    unittest.main()
