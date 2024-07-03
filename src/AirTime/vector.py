import math


class Vector:
    v: tuple[float, float, float]

    def __init__(self, *args) -> None:
        if len(args) == 1:
            self.v = tuple(args[0])
        elif len(args) == 3:
            self.v = (args[0], args[1], args[2])
        else:
            raise ValueError

    def __add__(self, o):
        return Vector(self.v[i] + o.v[i] for i in range(3))

    def __iadd__(self, o):
        self.v = tuple(self.v[i] + o.v[i] for i in range(3))
        return self

    def __sub__(self, o):
        return Vector(self.v[i] - o.v[i] for i in range(3))

    def __rsub__(self, o):
        return o - self

    def __isub__(self, o):
        self.v = tuple(self.v[i] - o.v[i] for i in range(3))
        return self

    def __neg__(self):
        return Vector(-self.v[i] for i in range(3))

    def __mul__(self, o):
        if isinstance(o, (int, float)):
            return Vector(self.v[i] * o for i in range(3))
        raise NotImplementedError

    def __rmul__(self, o):
        return self * o

    def __imul__(self, o):
        self.v = tuple(self.v[i] * o for i in range(3))
        return self

    def __truediv__(self, o):
        if isinstance(o, (int, float)):
            return Vector(self.v[i] / o for i in range(3))
        raise NotImplementedError

    def __rtruediv__(self, o):
        return o / self

    def __itruediv__(self, o):
        self.v = tuple(self.v[i] / o for i in range(3))
        return self

    def __str__(self):
        return f"({self.v[0]}, {self.v[1]}, {self.v[2]})"

    def __getitem__(self, i):
        return self.v[i]

    def length(self) -> float:
        return math.sqrt(sum(self.v[i] ** 2 for i in range(3)))


def dot(a: Vector, b: Vector) -> float:
    return sum(a[i] * b[i] for i in range(3))


def cross(a: Vector, b: Vector) -> Vector:
    return Vector(
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def norm(a: Vector) -> float:
    return a.length()
