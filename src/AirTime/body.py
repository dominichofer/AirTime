from dataclasses import dataclass
import math
import numpy as np
import glm
from .camera import Camera
from .matrix import Matrix, outer
from .vector import Vector, dot


class Body:
    "A body in 3D space"

    def __init__(self, pos, rot):
        self.pos = pos or Vector(0, 0, 0)
        self.rot = rot or Matrix.identity()

    def translate(self, v: Vector) -> None:
        self.pos += v

    def rotate(self, p: Vector, r: Matrix) -> None:
        "Rotate by Matrix r around point p"
        self.pos = r * (self.pos - p) + p
        self.rot = r * self.rot

    @property
    def mat4(self) -> glm.mat4:
        return glm.mat4(
            self.rot.m[0][0],
            self.rot.m[1][0],
            self.rot.m[2][0],
            0,
            self.rot.m[0][1],
            self.rot.m[1][1],
            self.rot.m[2][1],
            0,
            self.rot.m[0][2],
            self.rot.m[1][2],
            self.rot.m[2][2],
            0,
            self.pos.v[0],
            self.pos.v[1],
            self.pos.v[2],
            1,
        )


class RigidBody(Body):
    "A rigid body with mass and inertia tensor"

    def __init__(self, pos, rot, m: float, i: Matrix):
        Body.__init__(self, pos, rot)
        self.m = m  # Mass
        self.i = i  # Inertia tensor

    @property
    def center_of_mass(self) -> Vector:
        return self.pos

    def inertia_tensor_in(self, pos: Vector, rot: Matrix) -> Matrix:
        "Inertia tensor at point p"
        # Parallel axis theorem (https://en.wikipedia.org/wiki/Parallel_axis_theorem)
        delta_pos = pos - self.pos
        delta_rot = rot * self.rot.transposed()
        return delta_rot * self.i * delta_rot.transposed() + self.m * (
            dot(delta_pos, delta_pos) * Matrix.identity() - outer(delta_pos, delta_pos)
        )


@dataclass
class Color:
    red: float
    green: float
    blue: float


class GraphicalBody(Body):
    "A body that can be rendered"

    def __init__(self, ctx, pos, rot, points, triangles, shader, color: Color):
        super().__init__(pos, rot)

        v = np.array([points[i] for t in triangles for i in t], dtype="f4")
        n = [
            np.cross(v[i + 1] - v[i], v[i + 2] - v[i])
            for i in range(0, len(v), 3)
            for _ in range(3)
        ]
        self.vertex_buffer = ctx.buffer(np.hstack([v, n]))

        with open(f"shaders/{shader}.vert", "r", encoding="utf-8") as f:
            vertex_shader = f.read()
        with open(f"shaders/{shader}.frag", "r", encoding="utf-8") as f:
            fragment_shader = f.read()

        self.vertex_array = ctx.vertex_array(
            ctx.program(vertex_shader, fragment_shader),
            [(self.vertex_buffer, "3f 3f", "in_position", "in_normal")],
        )

        self.vertex_array.program["color"].write(
            glm.vec3(color.red, color.green, color.blue)
        )
        self.vertex_array.program["m_model"].write(self.mat4)

    def render(self, camera: Camera):
        self.vertex_array.program["m_proj"].write(camera.projection)
        self.vertex_array.program["m_view"].write(camera.view)
        self.vertex_array.program["m_model"].write(self.mat4)
        self.vertex_array.render()


class SimulationBody(RigidBody, GraphicalBody):
    "A body that is both a rigid body and a graphical body"

    def __init__(self, ctx, pos, rot, m, i, points, triangles, shader, color: Color):
        RigidBody.__init__(self, pos, rot, m, i)
        GraphicalBody.__init__(self, ctx, pos, rot, points, triangles, shader, color)


class Cube(SimulationBody):
    def __init__(
        self,
        ctx,
        a: float,
        b: float,
        c: float,
        color: Color,
        pos: Vector | None = None,
        rot: Matrix | None = None,
        shader: str = "default",
    ):
        m = a * b * c
        i = m * Matrix.from_diagonal(
            (b**2 + c**2) / 12, (a**2 + c**2) / 12, (a**2 + b**2) / 12
        )

        a /= 2
        b /= 2
        c /= 2
        points = [
            (-a, -b, c),
            (a, -b, c),
            (a, b, c),
            (-a, b, c),
            (-a, b, -c),
            (-a, -b, -c),
            (a, -b, -c),
            (a, b, -c),
        ]
        triangles = [
            (0, 2, 3),
            (0, 1, 2),
            (1, 7, 2),
            (1, 6, 7),
            (6, 5, 4),
            (4, 7, 6),
            (3, 4, 5),
            (3, 5, 0),
            (3, 7, 4),
            (3, 2, 7),
            (0, 6, 1),
            (0, 5, 6),
        ]
        SimulationBody.__init__(
            self, ctx, pos, rot, m, i, points, triangles, shader, color
        )


class Cylinder(SimulationBody):
    def __init__(
        self,
        ctx,
        a: float,
        b: float,
        h: float,
        color: Color,
        pos: Vector | None = None,
        rot: Matrix | None = None,
        shader: str = "default",
    ):
        m = math.pi * a * b * h
        i = m * Matrix.from_diagonal(
            b**2 / 4 + h**2 / 3, a**2 / 4 + h**2 / 3, (a**2 + b**2) / 4
        )

        a /= 2
        b /= 2
        h /= 2
        top_points = [
            (a * math.cos(2 * math.pi * i / 24), b * math.sin(2 * math.pi * i / 24), h)
            for i in range(24)
        ]
        bottom_points = [
            (
                a * math.cos(2 * math.pi * (i + 0.5) / 24),
                b * math.sin(2 * math.pi * (i + 0.5) / 24),
                -h,
            )
            for i in range(24)
        ]
        top_center = (0, 0, h)
        bottom_center = (0, 0, -h)
        points = top_points + bottom_points + [top_center, bottom_center]
        triangles = [((i + 1) % 24, i, i + 24) for i in range(24)]
        triangles += [(i + 24, (i + 1) % 24 + 24, (i + 1) % 24) for i in range(24)]
        triangles += [(i, (i + 1) % 24, 48) for i in range(24)]
        triangles += [((i + 1) % 24 + 24, i + 24, 49) for i in range(24)]
        SimulationBody.__init__(
            self, ctx, pos, rot, m, i, points, triangles, shader, color
        )


class Sphere(SimulationBody):
    def __init__(
        self,
        ctx,
        a: float,
        b: float,
        c: float,
        color: Color,
        pos: Vector | None = None,
        rot: Matrix | None = None,
        shader: str = "default",
    ):
        m = 0.75 * math.pi * a * b * c
        i = 0.4 * m * Matrix.from_diagonal((b**2 + c**2), (a**2 + c**2), (a**2 + b**2))

        a /= 2
        b /= 2
        c /= 2
        points = []
        for i in range(24):
            for j in range(12):
                points.append(
                    (
                        a
                        * math.sin(math.pi * j / 11)
                        * math.cos(2 * math.pi * (i + j / 2) / 24),
                        b
                        * math.sin(math.pi * j / 11)
                        * math.sin(2 * math.pi * (i + j / 2) / 24),
                        c * math.cos(math.pi * j / 11),
                    )
                )
        triangles = []
        for i in range(24):
            for j in range(12):
                triangles.append(
                    ((i + 1) % 24 * 12 + j, i * 12 + j, i * 12 + (j + 1) % 12)
                )
                triangles.append(
                    (
                        (i + 1) % 24 * 12 + (j + 1) % 12,
                        (i + 1) % 24 * 12 + j,
                        i * 12 + (j + 1) % 12,
                    )
                )
        SimulationBody.__init__(
            self, ctx, pos, rot, m, i, points, triangles, shader, color
        )


class MultiBody:
    "A collection of bodies"

    def __init__(self, bodies):
        self.bodies = bodies

    def translate(self, v: Vector) -> None:
        for body in self.bodies:
            body.translate(v)

    def rotate(self, p: Vector, r: Matrix) -> None:
        for body in self.bodies:
            body.rotate(p, r)

    @property
    def center_of_mass(self) -> Vector:
        m = sum(body.m for body in self.bodies)
        cm = Vector(0, 0, 0)
        for body in self.bodies:
            cm += body.m * body.center_of_mass
        return cm / m

    def inertia_tensor_at(self, p: Vector) -> Matrix:
        i = Matrix.zero()
        for body in self.bodies:
            i += body.inertia_tensor_at(p)
        return i

    def render(self, camera: Camera):
        for body in self.bodies:
            body.render(camera)
