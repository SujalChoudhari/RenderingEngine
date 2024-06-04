from OpenGL.GL import *
from OpenGL.GLU import *

from src.geometry.geometry import Geometry


class Line(Geometry):
    def __init__(self, origin, destination, update=None):
        super().__init__(position=[0,0,0],update_callback=update)
        self.p1 = origin
        self.p2 = destination

    def render(self, camera_position):
        self.apply_transformations()
        self.apply_color()
        glBegin(GL_LINES)
        glVertex3f(self.p1[0], self.p1[1], self.p1[2])
        glVertex3f(self.p2[0], self.p2[1], self.p2[2])
        glEnd()
