import math
from dataclasses import dataclass
from .matrix import Matrix
from .vector import Vector, norm


@dataclass
class Quaternion:
    w: float
    x: float
    y: float
    z: float

    @staticmethod
    def from_axis_angle(axis: Vector, angle: float) -> "Quaternion":
        n = norm(axis)
        if n == 0:
            return Quaternion(1, 0, 0, 0)
        axis /= n
        angle /= 2
        return Quaternion(math.cos(angle), axis[0] * math.sin(angle), axis[1] * math.sin(angle), axis[2] * math.sin(angle))

    def __add__(self, o):
        return Quaternion(self.w + o.w, self.x + o.x, self.y + o.y, self.z + o.z)

    def __sub__(self, o):
        return Quaternion(self.w - o.w, self.x - o.x, self.y - o.y, self.z - o.z)

    def __neg__(self):
        return Quaternion(-self.w, -self.x, -self.y, -self.z)

    def __mul__(self, o):
        if isinstance(o, (int, float)):
            return Quaternion(self.w * o, self.x * o, self.y * o, self.z * o)
        if isinstance(o, (Vector, Matrix)):
            return self.rotation_matrix() * o
        if isinstance(o, Quaternion):
            return Quaternion(
                +self.z * o.w - self.y * o.x + self.x * o.y + self.w * o.z,
                +self.y * o.w + self.z * o.x - self.w * o.y + self.x * o.z,
                -self.x * o.w + self.w * o.x + self.z * o.y + self.y * o.z,
                -self.w * o.w - self.x * o.x - self.y * o.y + self.z * o.z,
            )

    def __rmul__(self, o):
        if isinstance(o, (int, float, Vector, Matrix)):
            return o * self
        raise NotImplementedError

    def __str__(self):
        return f"({self.w}, {self.x}, {self.y}, {self.z})"

    def norm(self):
        return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)

    def axis(self):
        n = math.sqrt(self.w**2 + self.x**2 + self.y**2)
        if n == 0:
            return (0, 0, 0)
        return (self.w / n, self.x / n, self.y / n)

    def angle(self):
        n = self.norm()
        if n == 0:
            return 0
        return 2 * math.acos(self.z / n)

    def rotation_matrix(self):
        w, x, y, z = self.w, self.x, self.y, self.z
        return Matrix(
            1 - 2 * (x * x + y * y),
            2 * (w * x - y * z),
            2 * (w * y + x * z),
            2 * (w * x + y * z),
            1 - 2 * (w * w + y * y),
            2 * (x * y - w * z),
            2 * (w * y - x * z),
            2 * (w * z + x * y),
            1 - 2 * (w * w + x * x),
        )
