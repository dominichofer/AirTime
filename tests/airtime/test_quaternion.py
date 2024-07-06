import unittest
import math
from airtime import Vector, Quaternion, RotationQuaternion


class TestQuaternion(unittest.TestCase):
    def test_addition(self):
        q1 = Quaternion(1, 2, 3, 4)
        q2 = Quaternion(5, 6, 7, 8)
        result = q1 + q2
        self.assertEqual(result, Quaternion(6, 8, 10, 12))

    def test_subtraction(self):
        q1 = Quaternion(1, 2, 3, 4)
        q2 = Quaternion(5, 6, 7, 8)
        result = q1 - q2
        self.assertEqual(result, Quaternion(-4, -4, -4, -4))

    def test_multiplication(self):
        q1 = Quaternion(1, 2, 3, 4)
        q2 = Quaternion(5, 6, 7, 8)
        result = q1 * q2
        self.assertEqual(result, Quaternion(-60, 12, 30, 24))

    def test_division(self):
        q1 = Quaternion(1, 2, 3, 4)
        q2 = Quaternion(5, 6, 7, 8)
        q3 = q1 * q2
        result = q3 / q2
        self.assertAlmostEqual(result.a, q1.a)
        self.assertAlmostEqual(result.b, q1.b)
        self.assertAlmostEqual(result.c, q1.c)
        self.assertAlmostEqual(result.d, q1.d)

    def test_conjugated(self):
        q = Quaternion(1, 2, 3, 4)
        result = q.conjugated()
        self.assertEqual(result, Quaternion(1, -2, -3, -4))

    def test_norm(self):
        q = Quaternion(1, 2, 3, 4)
        result = q.norm()
        self.assertEqual(result, 5.477225575051661)

    def test_normalized(self):
        q = Quaternion(1, 2, 3, 4)
        result = q.normalized()
        self.assertEqual(
            result,
            Quaternion(
                0.18257418583505536,
                0.3651483716701107,
                0.5477225575051661,
                0.7302967433402214,
            ),
        )

    def test_reciprocal(self):
        q = Quaternion(1, 2, 3, 4)
        result = q.reciprocal()
        self.assertEqual(
            result,
            Quaternion(
                0.03333333333333333, -0.06666666666666667, -0.1, -0.13333333333333333
            ),
        )


class TestRotationQuaternion(unittest.TestCase):
    def test_axis(self):
        angle = 2 * math.pi / 3
        axis = Vector(1, 1, 1)
        q = RotationQuaternion(angle, axis)
        result = q.axis()
        self.assertTrue(result.isclose(axis.normalized()))

    def test_angle(self):
        angle = 2 * math.pi / 3
        axis = Vector(1, 1, 1)
        q = RotationQuaternion(angle, axis)
        result = q.angle()
        self.assertAlmostEqual(result, angle)

    def test_rotate(self):
        angle = 2 * math.pi / 3
        axis = Vector(1, 1, 1)
        q = RotationQuaternion(angle, axis)
        v = Vector(1, 0, 0)
        result = q.rotate(v)
        self.assertTrue(result.isclose(Vector(0, 1, 0)))


if __name__ == "__main__":
    unittest.main()
