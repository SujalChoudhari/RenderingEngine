from OpenGL.GL import *
from OpenGL.GLU import *

from src.maths.vector import Vec3
from src.geometry.geometry import Geometry
class Line(Geometry):
    def __init__(self,origin:Vec3,destination:Vec3,update=None):
        super().__init__(update)
        self.p1 = origin
        self.p2 = destination

    def render(self):
        glBegin(GL_LINES)
        glVertex3f(self.p1.x,self.p1.y,self.p1.z)
        glVertex3f(self.p2.x,self.p2.y,self.p2.z)
        glEnd()