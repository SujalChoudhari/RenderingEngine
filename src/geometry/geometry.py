from OpenGL.GL import *
import numpy as np


class Geometry:
    def __init__(
        self,
        position=(0.0, 0.0, 0.0),
        rotation=(0.0, 0.0, 0.0),
        color=(1.0, 1.0, 1.0, 1.0),
        update_callback=None,
    ):
        self.update_callback = update_callback
        self.translation = np.array(position)
        self.rotation = np.array(rotation)
        self.color = np.array(color)  # Default color: white with alpha 1.0

    def update(self):
        if self.update_callback:
            self.update_callback()

    def translate(self, x, y, z):
        self.translation += np.array([x, y, z])

    def rotate(self, x, y, z):
        self.rotation += np.array([x, y, z])

    def change_color(self, r, g, b, a=1.0):
        self.color = np.array([r, g, b, a])

    def change_position(self, x, y, z):
        self.translation = np.array([x, y, z])

    def change_rotation(self, x, y, z):
        self.rotation = np.array([x, y, z])
        self.recalculate_normals()


    def recalculate_normals(self):
        ...

    def apply_transformations(self):
        glTranslatef(*self.translation)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)

    def apply_color(self):
        glColor4f(self.color[0], self.color[1], self.color[2], self.color[3])

    def is_face_visible(self, face_normal, camera_direction, buffer=0.1):
        dot_product = np.dot(face_normal, camera_direction)
        return dot_product <= buffer

    def render(self, camera_direction):
        ...
