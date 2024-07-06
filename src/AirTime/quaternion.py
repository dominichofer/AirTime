import math
from dataclasses import dataclass
from .vector import Vector


@dataclass
class Quaternion:
    a: float
    b: float
    c: float
    d: float

    def __add__(self, o) -> "Quaternion":
        return Quaternion(self.a + o.a, self.b + o.b, self.c + o.c, self.d + o.d)

    def __sub__(self, o) -> "Quaternion":
        return Quaternion(self.a - o.a, self.b - o.b, self.c - o.c, self.d - o.d)

    def __neg__(self) -> "Quaternion":
        return Quaternion(-self.a, -self.b, -self.c, -self.d)

    def __mul__(self, o) -> "Quaternion":
        if isinstance(o, (int, float)):
            return Quaternion(self.a * o, self.b * o, self.c * o, self.d * o)
        if isinstance(o, Quaternion):
            return Quaternion(
                self.a * o.a - self.b * o.b - self.c * o.c - self.d * o.d,
                self.a * o.b + self.b * o.a + self.c * o.d - self.d * o.c,
                self.a * o.c - self.b * o.d + self.c * o.a + self.d * o.b,
                self.a * o.d + self.b * o.c - self.c * o.b + self.d * o.a,
            )
        raise NotImplementedError

    def __rmul__(self, o) -> "Quaternion":
        if isinstance(o, (int, float)):
            return o * self
        raise NotImplementedError

    def __truediv__(self, o):
        if isinstance(o, (int, float)):
            return Quaternion(self.a / o, self.b / o, self.c / o, self.d / o)
        if isinstance(o, Quaternion):
            return self * o.reciprocal()
        raise NotImplementedError

    def __str__(self) -> str:
        return f"Quaternion({self.a}, {self.b}, {self.c}, {self.d})"

    def conjugated(self) -> "Quaternion":
        return Quaternion(self.a, -self.b, -self.c, -self.d)

    def norm(self) -> float:
        return math.sqrt(self.a**2 + self.b**2 + self.c**2 + self.d**2)

    def normalized(self) -> "Quaternion":
        n = self.norm()
        return self / n

    def reciprocal(self):
        return self.conjugated() / self.norm()**2


class RotationQuaternion(Quaternion):
    def __init__(self, angle: float, axis: Vector):
        a = math.cos(angle / 2)
        b, c, d = math.sin(angle / 2) * axis.normalized()
        super().__init__(a, b, c, d)

    def axis(self) -> Vector:
        return Vector(self.b, self.c, self.d).normalized()

    def angle(self) -> float:
        return 2 * math.atan2(Vector(self.b, self.c, self.d).length(), self.a)

    def rotate(self, v: Vector) -> Vector:
        q = Quaternion(0, *v)
        r = self * q * self.conjugated()
        return Vector(r.b, r.c, r.d)

    def __str__(self) -> str:
        return f"RotationQuaternion({self.a}, {self.b}, {self.c}, {self.d})"
