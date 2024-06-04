from OpenGL.GL import *
from src.geometry.geometry import Geometry
import numpy as np

class Cube(Geometry):
    def __init__(self, position, size, update=None):
        super().__init__(position=position, update_callback=update)
        self.size = size
        self.vertices = [
            (0, 0, 0),
            (size[0], 0, 0),
            (size[0], size[1], 0),
            (0, size[1], 0),
            (0, 0, size[2]),
            (size[0], 0, size[2]),
            (size[0], size[1], size[2]),
            (0, size[1], size[2]),
        ]

        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom edges
            (4, 5), (5, 6), (6, 7), (7, 4),  # Top edges
            (0, 4), (1, 5), (2, 6), (3, 7)   # Vertical edges
        ]

        self.surfaces = [
            (0, 1, 2, 3),  # Front face
            (4, 5, 6, 7),  # Back face
            (0, 1, 5, 4),  # Bottom face
            (3, 2, 6, 7),  # Top face
            (0, 3, 7, 4),  # Left face
            (1, 2, 6, 5)   # Right face
        ]

        self.normals = [
            (0, 0, -1),  # Front face
            (0, 0, 1),   # Back face
            (0, -1, 0),  # Bottom face
            (0, 1, 0),   # Top face
            (-1, 0, 0),  # Left face
            (1, 0, 0)    # Right face
        ]

        self._original_normals = list(self.normals)

    def recalculate_normals(self):
        rotation_matrix = self.get_rotation_matrix()
        for i, normal in enumerate(self._original_normals):
            normal = np.dot(rotation_matrix, np.array(normal + (0,)))[:3]  # Apply rotation
            normal = normal / np.linalg.norm(normal)  # Normalize the normal
            self.normals[i] = tuple(normal)

    def get_rotation_matrix(self):
        angle = np.radians(self.rotation)
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)

        # Assuming rotation order is x, y, z
        rx = np.array([
            [1, 0, 0, 0],
            [0, cos_a[0], -sin_a[0], 0],
            [0, sin_a[0], cos_a[0], 0],
            [0, 0, 0, 1]
        ])

        ry = np.array([
            [cos_a[1], 0, sin_a[1], 0],
            [0, 1, 0, 0],
            [-sin_a[1], 0, cos_a[1], 0],
            [0, 0, 0, 1]
        ])

        rz = np.array([
            [cos_a[2], -sin_a[2], 0, 0],
            [sin_a[2], cos_a[2], 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        rotation_matrix = np.dot(np.dot(rz, ry), rx)
        return rotation_matrix

    def render(self, camera_pos):
        glPushMatrix()
        self.apply_transformations()
        self.apply_color()
        glBegin(GL_QUADS)
        for i, surface in enumerate(self.surfaces):
            normal = self.normals[i]
            glNormal3fv(normal)
            if not self.is_face_visible(normal, camera_pos):
                continue
            for vertex in surface:
                v = self.vertices[vertex]
                glVertex3fv(v)
        glEnd()
        glPopMatrix()