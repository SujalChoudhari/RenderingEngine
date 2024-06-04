import math
from OpenGL.GL import *
from src.geometry.geometry import Geometry

class Sphere(Geometry):
    def __init__(self, position, radius, update=None, slices=15, stacks=15):
        super().__init__(position=position,update_callback=update)
        self.radius = radius
        self._slices = slices
        self._stacks = stacks
        self.generate_vertices()

    @property
    def slices(self):
        return self._slices
    
    @slices.setter
    def slices(self, value):
        self._slices = value
        self.generate_vertices()

    @property
    def stacks(self):
        return self._stacks
    
    @stacks.setter
    def stacks(self, value):
        self._stacks = value
        self.generate_vertices()

    def generate_vertices(self):
        self.vertices = []
        self.normals = []
        
        phi_step = math.pi / self._stacks
        theta_step = 2 * math.pi / self._slices

        for i in range(self._stacks + 1):
            phi = i * phi_step
            sin_phi = math.sin(phi)
            cos_phi = math.cos(phi)

            for j in range(self._slices + 1):
                theta = j * theta_step
                sin_theta = math.sin(theta)
                cos_theta = math.cos(theta)

                x = 0 + self.radius * sin_phi * cos_theta
                y = 0 + self.radius * sin_phi * sin_theta
                z = 0 + self.radius * cos_phi

                self.vertices.append((x, y, z))
                self.normals.append((sin_phi * cos_theta, sin_phi * sin_theta, cos_phi))

    def render(self, camera_position):
        glPushMatrix()
        self.apply_transformations()

        for i in range(self._stacks):
            for j in range(self._slices):
                index1 = i * (self._slices + 1) + j
                index2 = index1 + self._slices + 1

                normal1 = self.normals[index1]
                normal2 = self.normals[index2]
                
                if not self.is_face_visible(normal1, camera_position) or not self.is_face_visible(normal2, camera_position):
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