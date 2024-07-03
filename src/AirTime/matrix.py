import math
from dataclasses import dataclass
from .vector import Vector, norm


@dataclass
class Matrix:
    m: tuple[
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float],
    ]

    def __init__(self, *args) -> None:
        if len(args) == 0:
            self.m = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
        elif len(args) == 1:
            self.m = args[0]
        elif len(args) == 9:
            self.m = (
                (args[0], args[1], args[2]),
                (args[3], args[4], args[5]),
                (args[6], args[7], args[8]),
            )
        else:
            raise ValueError

    @staticmethod
    def identity() -> "Matrix":
        return Matrix(1, 0, 0, 0, 1, 0, 0, 0, 1)

    @staticmethod
    def zero() -> "Matrix":
        return Matrix(0, 0, 0, 0, 0, 0, 0, 0, 0)

    @staticmethod
    def from_diagonal(d: float, e: float, f: float) -> "Matrix":
        return Matrix(d, 0, 0, 0, e, 0, 0, 0, f)

    @staticmethod
    def from_euler(phi: float, theta: float, psi: float) -> "Matrix":
        c1 = math.cos(phi)
        s1 = math.sin(phi)
        c2 = math.cos(theta)
        s2 = math.sin(theta)
        c3 = math.cos(psi)
        s3 = math.sin(psi)
        return Matrix(
            c2 * c3, -c2 * s3, s2,
            c1 * s3 + c3 * s1 * s2, c1 * c3 - s1 * s2 * s3, -c2 * s1,
            s1 * s3 - c1 * c3 * s2, c3 * s1 + c1 * s2 * s3, c1 * c2
        )

    @staticmethod
    def from_axis_angle(axis: Vector, angle: float) -> "Matrix":
        n = norm(axis)
        if n == 0:
            raise ValueError
        c = math.cos(angle)
        s = math.sin(angle)
        t = 1 - c
        x = axis[0] / n
        y = axis[1] / n
        z = axis[2] / n
        return Matrix(
            t * x**2 + c, t * x * y - s * z, t * x * z + s * y,
            t * x * y + s * z, t * y**2 + c, t * y * z - s * x,
            t * x * z - s * y, t * y * z + s * x, t * z**2 + c
        )

    @staticmethod
    def from_axis(axis: Vector) -> "Matrix":
        return Matrix.from_axis_angle(axis, norm(axis))

    def __add__(self, o):
        return Matrix(
            tuple(tuple(self.m[i][j] + o.m[i][j] for j in range(3)) for i in range(3))
        )

    def __sub__(self, o):
        return Matrix(
            tuple(tuple(self.m[i][j] - o.m[i][j] for j in range(3)) for i in range(3))
        )

    def __neg__(self):
        return Matrix(tuple(tuple(-self.m[i][j] for j in range(3)) for i in range(3)))

    def __mul__(self, o):
        if isinstance(o, (int, float)):
            return Matrix(
                tuple(tuple(self.m[i][j] * o for j in range(3)) for i in range(3))
            )
        if isinstance(o, Vector):
            return Vector(sum(self.m[i][j] * o[j] for j in range(3)) for i in range(3))
        if isinstance(o, Matrix):
            return Matrix(
                tuple(
                    tuple(
                        sum(self.m[i][k] * o.m[k][j] for k in range(3))
                        for j in range(3)
                    )
                    for i in range(3)
                )
            )
        raise NotImplementedError

    def __rmul__(self, o):
        if isinstance(o, (int, float)):
            return self * o
        raise NotImplementedError

    def __str__(self):
        m = self.m
        return f"({m[0][0]}, {m[0][1]}, {m[0][2]})\n({m[1][0]}, {m[1][1]}, {m[1][2]})\n({m[2][0]}, {m[2][1]}, {m[2][2]})"

    def __getitem__(self, i):
        return self.m[i]

    def transposed(self) -> "Matrix":
        m = self.m
        return Matrix(
            m[0][0], m[1][0], m[2][0],
            m[0][1], m[1][1], m[2][1],
            m[0][2], m[1][2], m[2][2],
        )

    def inv(self) -> "Matrix":
        m = self.m
        det = (
            m[0][0] * m[1][1] * m[2][2]
            + m[0][1] * m[1][2] * m[2][0]
            + m[0][2] * m[1][0] * m[2][1]
            - m[0][2] * m[1][1] * m[2][0]
            - m[0][1] * m[1][0] * m[2][2]
            - m[0][0] * m[1][2] * m[2][1]
        )
        if det == 0:
            raise ValueError
        return Matrix(
            (m[1][1] * m[2][2] - m[1][2] * m[2][1]) / det,
            (m[0][2] * m[2][1] - m[0][1] * m[2][2]) / det,
            (m[0][1] * m[1][2] - m[0][2] * m[1][1]) / det,
            (m[1][2] * m[2][0] - m[1][0] * m[2][2]) / det,
            (m[0][0] * m[2][2] - m[0][2] * m[2][0]) / det,
            (m[0][2] * m[1][0] - m[0][0] * m[1][2]) / det,
            (m[1][0] * m[2][1] - m[1][1] * m[2][0]) / det,
            (m[0][1] * m[2][0] - m[0][0] * m[2][1]) / det,
            (m[0][0] * m[1][1] - m[0][1] * m[1][0]) / det,
        )


def outer(a: Vector, b: Vector) -> Matrix:
    return Matrix(
        a[0] * b[0],
        a[0] * b[1],
        a[0] * b[2],
        a[1] * b[0],
        a[1] * b[1],
        a[1] * b[2],
        a[2] * b[0],
        a[2] * b[1],
        a[2] * b[2],
    )
