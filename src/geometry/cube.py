from src.maths.vector import Vec3
from OpenGL.GL import *

from src.geometry.geometry import Geometry

class Cube(Geometry):
    def __init__(self, position, size, update=None):
        super().__init__(update)
        self.position = position
        self.size = size
        self.vertices = [
            Vec3(position.x, position.y, position.z),
            Vec3(position.x + size.x, position.y, position.z),
            Vec3(position.x + size.x, position.y + size.y, position.z),
            Vec3(position.x, position.y + size.y, position.z),
            Vec3(position.x, position.y, position.z + size.z),
            Vec3(position.x + size.x, position.y, position.z + size.z),
            Vec3(position.x + size.x, position.y + size.y, position.z + size.z),
            Vec3(position.x, position.y + size.y, position.z + size.z),
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
            Vec3(0, 0, -1),  # Front face
            Vec3(0, 0, 1),   # Back face
            Vec3(0, -1, 0),  # Bottom face
            Vec3(0, 1, 0),   # Top face
            Vec3(-1, 0, 0),  # Left face
            Vec3(1, 0, 0)    # Right face
        ]

    def render(self):
        glPushMatrix()
        self.apply_transformations()
        
        glBegin(GL_QUADS)
        for i, surface in enumerate(self.surfaces):
            normal = self.normals[i].to_tuple()
            glNormal3fv(normal)
            for vertex in surface:
                v = self.vertices[vertex].to_tuple()
                glVertex3fv(v)
        glEnd()
        
        glPopMatrix()
