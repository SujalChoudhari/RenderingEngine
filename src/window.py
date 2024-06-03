import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
class Window:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.is_active = True
        
        pygame.init()
        pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption(self.title)
        
        self.init_3d()

    def init_3d(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK , GL_AMBIENT_AND_DIFFUSE)
        glDepthFunc(GL_LEQUAL)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45.0, float(self.width) / float(self.height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def update(self):
        pygame.display.flip()

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def wait_for_close(self):
        return self.is_active

    def close(self):
        self.is_active = False