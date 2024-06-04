import math
import numpy as np
from OpenGL.GL import *
from src.geometry.geometry import Geometry
from src.geometry.circle import Circle


class Cylinder(Geometry):
    def __init__(self, position, radius, height, sides=20, update=None):
        super().__init__(position=position, update_callback=update)
        self.radius = radius
        self.height = height
        self.sides = sides

        self.bottom_circle = Circle(
            [0, 0, 0],
            radius,
            normal=(0, 0, -1),
            segments=sides,
        )
        self.top_circle = Circle(
            [0, 0, height],
            radius,
            normal=(0, 0, 1),
            segments=sides,
        )

        self.normals = [(0, 0, -1), (0, 0, 1)]  # Normals for bottom and top faces

    @property
    def num_segments(self):
        return self.sides
    
    @num_segments.setter
    def num_segments(self, value):
        self.sides = value
        self.bottom_circle.num_segments = value
        self.top_circle.num_segments = value

    def change_color(self, r, g, b, a=1.0):
        self.top_circle.change_color(r, g, b, a)
        self.bottom_circle.change_color(r, g, b, a)
        return super().change_color(r, g, b, a)

    def change_position(self, position):
        return super().change_position(position)

    def recalculate_normals(self):
        rotation_matrix = self.get_rotation_matrix()
        # Rotate bottom and top face normals
        self.normals = [
            tuple(np.dot(rotation_matrix, np.array((0, 0, -1) + (0,)))[:3]),
            tuple(np.dot(rotation_matrix, np.array((0, 0, 1) + (0,)))[:3]),
        ]

    def render(self, camera_pos):
        glPushMatrix()
        self.apply_transformations()
        self.apply_color()

        # Recalculate normals before rendering
        self.recalculate_normals()

        # Render bottom circle
        if self.is_face_visible(self.normals[0], camera_pos):
            self.bottom_circle.render(camera_pos)

        # Render top circle
        if self.is_face_visible(self.normals[1], camera_pos):
            self.top_circle.render(camera_pos)

        # Render side faces
        glBegin(GL_QUAD_STRIP)
        rotation_matrix = self.get_rotation_matrix()
        for i in range(self.sides + 1):
            theta = 2 * math.pi * i / self.sides
            x = self.radius * math.cos(theta)
            y = self.radius * math.sin(theta)
            z1 = 0
            z2 = self.height

            # Calculate normal for the side face
            nx = math.cos(theta)
            ny = math.sin(theta)
            normal = np.dot(rotation_matrix, np.array((nx, ny, 0) + (0,)))[:3]
            normal = tuple(normal / np.linalg.norm(normal))  # Normalize the normal
            glNormal3fv(normal)

            glVertex3f(x, y, z1)
            glVertex3f(x, y, z2)
        glEnd()

        glPopMatrix()
