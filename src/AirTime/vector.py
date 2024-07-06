import math
from dataclasses import dataclass


@dataclass
class Vector:
    x: float
    y: float
    z: float

    def __add__(self, o) -> "Vector":
        return Vector(self.x + o.x, self.y + o.y, self.z + o.z)

    def __iadd__(self, o) -> "Vector":
        self.x += o.x
        self.y += o.y
        self.z += o.z
        return self

    def __sub__(self, o) -> "Vector":
        return Vector(self.x - o.x, self.y - o.y, self.z - o.z)

    def __rsub__(self, o) -> "Vector":
        return Vector(o.x - self.x, o.y - self.y, o.z - self.z)

    def __isub__(self, o) -> "Vector":
        self.x -= o.x
        self.y -= o.y
        self.z -= o.z
        return self

    def __neg__(self) -> "Vector":
        return Vector(-self.x, -self.y, -self.z)

    def __mul__(self, o) -> "Vector":
        if isinstance(o, (int, float)):
            return Vector(self.x * o, self.y * o, self.z * o)
        raise NotImplementedError

    def __rmul__(self, o) -> "Vector":
        if isinstance(o, (int, float)):
            return self * o
        raise NotImplementedError

    def __imul__(self, o) -> "Vector":
        self.x *= o
        self.y *= o
        self.z *= o
        return self

    def __truediv__(self, o) -> "Vector":
        if isinstance(o, (int, float)):
            return Vector(self.x / o, self.y / o, self.z / o)
        raise NotImplementedError

    def __rtruediv__(self, o) -> "Vector":
        return Vector(o.x / self.x, o.y / self.y, o.z / self.z)

    def __itruediv__(self, o) -> "Vector":
        self.x /= o
        self.y /= o
        self.z /= o
        return self

    def __str__(self) -> str:
        return f"Vector({self.x}, {self.y}, {self.z})"

    def __getitem__(self, i: int) -> float:
        return (self.x, self.y, self.z)[i]

    def length(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalized(self) -> "Vector":
        return self / self.length()
    
    def isclose(self, o: "Vector", tol: float = 1e-6) -> bool:
        return all(abs(self[i] - o[i]) < tol for i in range(3))


def dot(a: Vector, b: Vector) -> float:
    return a.x * b.x + a.y * b.y + a.z * b.z


def cross(a: Vector, b: Vector) -> Vector:
    return Vector(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)


def norm(a: Vector) -> float:
    return a.length()


def angle_between(a: Vector, b: Vector) -> float:
    return math.acos(dot(a, b) / (a.length() * b.length()))
