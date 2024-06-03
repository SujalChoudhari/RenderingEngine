import math
from OpenGL.GL import *
from src.geometry.geometry import Geometry

class Sphere(Geometry):
    def __init__(self, position, radius, update=None, slices=15, stacks=15):
        super().__init__(update)
        self.position = position
        self.radius = radius
        self.slices = slices
        self.stacks = stacks
        self.generate_vertices()

    def change_position(self, position):
        self.position = position
        self.generate_vertices()
        return super().change_position(position)

    def generate_vertices(self):
        self.vertices = []
        self.normals = []
        
        phi_step = math.pi / self.stacks
        theta_step = 2 * math.pi / self.slices

        for i in range(self.stacks + 1):
            phi = i * phi_step
            sin_phi = math.sin(phi)
            cos_phi = math.cos(phi)

            for j in range(self.slices + 1):
                theta = j * theta_step
                sin_theta = math.sin(theta)
                cos_theta = math.cos(theta)

                x = self.position[0] + self.radius * sin_phi * cos_theta
                y = self.position[1] + self.radius * sin_phi * sin_theta
                z = self.position[2] + self.radius * cos_phi

                self.vertices.append((x, y, z))
                self.normals.append((sin_phi * cos_theta, sin_phi * sin_theta, cos_phi))

    def render(self, camera_position):
        glPushMatrix()
        self.apply_transformations()

        for i in range(self.stacks):
            for j in range(self.slices):
                index1 = i * (self.slices + 1) + j
                index2 = index1 + self.slices + 1

                normal1 = self.normals[index1]
                normal2 = self.normals[index2]
                
                if not self.is_face_visible(normal1, camera_position):
                    continue

                glBegin(GL_QUADS)
                glNormal3fv(self.normals[index1])
                glVertex3fv(self.vertices[index1])
                glNormal3fv(self.normals[index2])
                glVertex3fv(self.vertices[index2])
                glNormal3fv(self.normals[index2 + 1])
                glVertex3fv(self.vertices[index2 + 1])
                glNormal3fv(self.normals[index1 + 1])
                glVertex3fv(self.vertices[index1 + 1])
                glEnd()

        glPopMatrix()