from .matrix import Matrix
from .vector import Vector, cross
from .body import RigidBody


class RotatingBody:
    def __init__(self, body: RigidBody, w: Vector):
        "w is the angular velocity of the body in radians per second"
        self.body = body
        self.w = w

    def time_step(self, delta_time: int):
        # https://en.wikipedia.org/wiki/Euler%27s_equations_(rigid_body_dynamics)
        cm = self.body.center_of_mass
        i = self.body.inertia_tensor_in(cm)
        self.w -= i.inv() * (cross(self.w, i * self.w)) * delta_time
        rot = Matrix.from_axis_angle(self.w, self.w.length() * delta_time)
        self.body.rotate(cm, rot)

    def render(self, camera):
        self.body.render(camera)
