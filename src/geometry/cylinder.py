import math
from OpenGL.GL import *
from src.geometry.geometry import Geometry
from src.geometry.circle import Circle


class Cylinder(Geometry):
    def __init__(self, position, radius, height, sides=20, update=None):
        super().__init__(update)
        self.position = position
        self.radius = radius
        self.height = height
        self.sides = sides

        self.bottom_circle = Circle(
            (position[0], position[1], position[2]),
            radius,
            normal=(0, 0, -1),
            segments=sides,
        )
        self.top_circle = Circle(
            (position[0], position[1], position[2] + height),
            radius,
            normal=(0, 0, 1),
            segments=sides,
        )

        self.normals = [(0, 0, -1), (0, 0, 1)]  # Normals for bottom and top faces

    def set_color(self, r, g, b, a=1.0):
        self.top_circle.set_color(r, g, b, a)
        self.bottom_circle.set_color(r, g, b, a)
        return super().set_color(r, g, b, a)


    def render(self, camera_pos):
        glPushMatrix()
        self.apply_transformations()
        self.apply_color()
        # Render bottom circle
        if self.is_face_visible((0, 0, -1), camera_pos):
            self.bottom_circle.render(camera_pos)

        # Render top circle
        if self.is_face_visible((0, 0, 1), camera_pos):
            self.top_circle.render(camera_pos)

        # Render side faces
        glBegin(GL_QUAD_STRIP)
        for i in range(self.sides + 1):
            theta = 2 * math.pi * i / self.sides
            x = self.position[0] + self.radius * math.cos(theta)
            y = self.position[1] + self.radius * math.sin(theta)
            z1 = self.position[2]
            z2 = self.position[2] + self.height

            # Calculate normal for the side face
            nx = math.cos(theta)
            ny = math.sin(theta)
            normal = (nx, ny, 0)
            if self.is_face_visible(normal, camera_pos):
                glNormal3fv(normal)
                glVertex3f(x, y, z1)
                glVertex3f(x, y, z2)
        glEnd()

        glPopMatrix()
