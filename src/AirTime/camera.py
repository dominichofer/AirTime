import glm
import pygame as pg


class Camera:
    def __init__(self, aspect_ratio):
        self.aspect_ratio = aspect_ratio
        self.azimuth = 0
        self.elevation = 0
        self.distance = 20

    def update(self, delta_time):
        velocity = delta_time * 0.001
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.elevation += velocity
        if keys[pg.K_s]:
            self.elevation -= velocity
        if keys[pg.K_a]:
            self.azimuth -= velocity
        if keys[pg.K_d]:
            self.azimuth += velocity
        if keys[pg.K_LSHIFT]:
            self.distance += velocity * 10
        if keys[pg.K_LCTRL]:
            self.distance -= velocity * 10

        for event in pg.event.get(pg.MOUSEWHEEL):
            self.distance -= event.y * 0.2

        self.elevation = glm.clamp(self.elevation, -1.57, 1.57)

    @property
    def view(self):
        pos = glm.vec3(
            self.distance * glm.cos(self.elevation) * glm.sin(self.azimuth),
            self.distance * glm.sin(self.elevation),
            self.distance * glm.cos(self.elevation) * glm.cos(self.azimuth),
        )
        return glm.lookAt(pos, glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))

    @property
    def projection(self):
        field_of_view = glm.radians(50)
        near = 0.1
        far = 100
        return glm.perspective(field_of_view, self.aspect_ratio, near, far)
