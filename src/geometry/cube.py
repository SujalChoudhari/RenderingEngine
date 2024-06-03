from OpenGL.GL import *

from src.geometry.geometry import Geometry

class Cube(Geometry):
    def __init__(self, position, size, update=None):
        super().__init__(update)
        self.position = position
        self.size = size
        self.vertices = [
            (position[0], position[1], position[2]),
            (position[0] + size[0], position[1], position[2]),
            (position[0] + size[0], position[1] + size[1], position[2]),
            (position[0], position[1] + size[1], position[2]),
            (position[0], position[1], position[2] + size[2]),
            (position[0] + size[0], position[1], position[2] + size[2]),
            (position[0] + size[0], position[1] + size[1], position[2] + size[2]),
            (position[0], position[1] + size[1], position[2] + size[2]),
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

    def render(self,camera_pos):
        glPushMatrix()
        self.apply_transformations()
        
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
