from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from src.geometry.geometry import Geometry

class Light(Geometry):
    def __init__(self, position, ambient, diffuse, specular, light_id=GL_LIGHT0):
        super().__init__()
        self.position = np.array(position)
        self.ambient = np.array(ambient)
        self.diffuse = np.array(diffuse)
        self.specular = np.array(specular)
        self.light_id = light_id

    def render(self,camera_position):
        glEnable(GL_LIGHTING)
        glEnable(self.light_id)

        glLightfv(self.light_id, GL_POSITION, [self.position[0], self.position[1], self.position[2], 1.0])
        glLightfv(self.light_id, GL_AMBIENT, self.ambient)
        glLightfv(self.light_id, GL_DIFFUSE, self.diffuse)
        glLightfv(self.light_id, GL_SPECULAR, self.specular)

    def disable(self):
        glDisable(self.light_id)
        glDisable(GL_LIGHTING)
