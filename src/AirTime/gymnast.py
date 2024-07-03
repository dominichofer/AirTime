from .body import Color, Cube, Cylinder, Sphere, MultiBody
from .joint import HingeJoint
from .vector import Vector
from .matrix import Matrix

PI = 3.14159265358979323846


class Gymnast(MultiBody):
    def __init__(self, ctx):
        cube1 = Cube(ctx, 1, 8, 8, Color(0, 0.5, 1))
        cube2 = Cube(ctx, 4, 1, 1, Color(0, 0.5, 0), pos=Vector(2.5, -3.5, 4.5))
        self.hinge = HingeJoint(
            ctx,
            1,
            1,
            Color(1, 0, 0),
            cube2,
            cube1,
            axis=Vector(0, 1, 0),
            angle=PI / 2,
            pos=Vector(0.5, -3.5, 4),
            rot=Matrix.identity(),
        )
        bodies = [cube1, cube2, self.hinge]
        MultiBody.__init__(self, bodies)

    def time_step(self, delta_time):
        self.hinge.bend(-0.01)
