import sys
import pygame as pg
import moderngl as mgl
from AirTime.camera import Camera
from AirTime.gymnast import Gymnast
from AirTime.rotating_body import RotatingBody
from AirTime.vector import Vector


class GraphicsEngine:
    def __init__(self, win_size=(800, 600)):
        pg.init()
        self.WIN_SIZE = win_size

        # set opengl version
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(
            pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE
        )
        pg.display.set_mode(self.WIN_SIZE, pg.DOUBLEBUF | pg.OPENGL)

        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)

        self.clock = pg.time.Clock()
        self.delta_time = 0

        self.camera = Camera(aspect_ratio=win_size[0] / win_size[1])
        self.body = Gymnast(self.ctx)

    def check_events(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE] or pg.event.get(pg.QUIT):
            pg.quit()
            sys.exit()

    def render(self):
        self.ctx.clear(0, 0, 0)
        self.body.render(self.camera)
        pg.display.flip()

    def run(self):
        while True:
            self.render()
            self.check_events()
            self.body.time_step(self.delta_time)
            self.camera.update(self.delta_time)
            self.delta_time = self.clock.tick(60)


if __name__ == "__main__":
    app = GraphicsEngine()
    app.run()
