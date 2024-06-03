import math
from OpenGL.GL import *
from src.geometry.geometry import Geometry


class Circle(Geometry):
    def __init__(self, position, radius, update=None,normal=(0,0,1), segments=32):
        super().__init__(update)
        self.position = position
        self.radius = radius
        self.segments = segments
        self.normal = normal  # Normal along the z-axis for the circle
        self.vertices = []

        for i in range(segments + 1):
            theta = 2 * math.pi * i / segments
            x = self.position[0] + self.radius * math.cos(theta)
            y = self.position[1] + self.radius * math.sin(theta)
            z = self.position[2]
            self.vertices.append((x, y, z))

    def render(self, camera_direction):        
        glPushMatrix()
        self.apply_transformations()
        self.apply_color()
        if self.is_face_visible(self.normal, camera_direction):
            glBegin(GL_POLYGON)
            glNormal3fv(self.normal)
            for vertex in self.vertices:
                glVertex3fv(vertex)
            glEnd()

        glPopMatrix()
