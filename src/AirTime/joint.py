import numpy as np
from dataclasses import dataclass
from .body import Color, Body, RigidBody, GraphicalBody, Cylinder, Sphere
from .matrix import Matrix
from .vector import Vector


class Joint(Body):
    def __init__(self, pos, rot, first: RigidBody, second: RigidBody):
        Body.__init__(self, pos, rot)
        self.first = first
        self.second = second


class HingeJoint(Joint, Cylinder):
    def __init__(
        self,
        ctx,
        radius: float,
        height: float,
        color: Color,
        first: RigidBody,
        second: RigidBody,
        axis: Vector,  # Axis of rotation
        angle: float,
        pos,
        rot,
    ):
        Joint.__init__(self, pos, rot, first, second)
        Cylinder.__init__(self, ctx, radius, radius, height, color, pos, rot)
        self.axis = axis
        self.angle = angle

    def bend(self, angle: float) -> None:
        "Bend by angle around axis of rotation"
        self.angle += angle
        # In the coordinate system of joint, such that that the axis of rotation is the z-axis
        # ( T_x)         (alpha_x)
        # ( T_y) = I_A * (alpha_y)
        # ( T_z)         (alpha_A)
        #
        # ( T_x)         (alpha_x)
        # ( T_y) = I_B * (alpha_y)
        # (-T_z)         (alpha_B)

        I_a = self.first.inertia_tensor_in(self.pos, self.rot)
        I_b = self.second.inertia_tensor_in(self.pos, self.rot)

        A = np.array(
            [
                [I_a[0][0], I_a[0][1], I_a[0][2], 0, -1, 0],
                [I_a[1][0], I_a[1][1], I_a[1][2], 0, 0, -1],
                [I_a[2][0], I_a[2][1], I_a[2][2], 0, 0, 0],
                [I_b[0][0], I_b[0][1], 0, I_b[0][2], -1, 0],
                [I_b[1][0], I_b[1][1], 0, I_b[1][2], 0, -1],
                [I_b[2][0], I_b[2][1], 0, I_b[2][2], 0, 0],
            ]
        )
        b = np.array([0, 0, 1, 0, 0, -1])
        x = np.linalg.solve(A, b)
        alpha_x = x[0]
        alpha_y = x[1]
        alpha_A = x[2]
        alpha_B = x[3]

        scale = angle / (alpha_B - alpha_A)

        to_global = self.rot.transposed()
        rot = Matrix.from_axis(to_global * Vector(alpha_x * scale, alpha_y * scale, 0))
        rotA = Matrix.from_axis(to_global * Vector(0, 0, alpha_A * scale))
        rotB = Matrix.from_axis(to_global * Vector(0, 0, alpha_B * scale))
        self.first.rotate(self.pos, rotA)
        self.second.rotate(self.pos, rotB)
        self.first.rotate(self.pos, rot)
        self.second.rotate(self.pos, rot)
        self.rotate(self.pos, rot)


@dataclass
class SaddleJoint(Joint):
    axis_a: Vector  # Axis of rotation
    axis_b: Vector  # Axis of rotation
    angle_a: float = 0
    angle_b: float = 0


@dataclass
class BallJoint(Joint):
    phi: float = 0
    theta: float = 0
    psi: float = 0

    def bend(self, phi: float, theta: float, psi: float) -> None:
        "Bend by angles"
        # self.phi += phi
        # self.theta += theta
        # self.psi += psi
        # Ia = self.first.inertia_tensor_at(self.pos)
        # Ib = self.second.inertia_tensor_at(self.pos)
        # # TODO: Implement physics
        # angle_a = 0
        # angle_b = 0
        # self.first.rotate(self.x, Matrix.from_axis_angle(self.axis, angle_a))
        # self.second.rotate(self.x, Matrix.from_axis_angle(self.axis, angle_b))
