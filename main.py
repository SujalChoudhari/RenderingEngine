import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from src.window import Window
from src.renderer import Renderer
from src.geometry.line import Line
from src.geometry.cube import Cube
from src.geometry.sphere import Sphere
from src.geometry.cylinder import Cylinder
from src.geometry.light import Light
from src.free_camera import FreeCamera

class Application:
    def __init__(self):
        pygame.init()
        self.window = Window(800, 600, "Hello World")
        self.renderer = Renderer()
        self.clock = pygame.time.Clock()
        self.camera = FreeCamera([0, 0, 3], [0, 0, -1], [0, 1, 0])
        self.initialize_objects()
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

    def initialize_objects(self):
        the_cube = Cube((-0.5, -0.5, -5), (1, 1, 1))
        the_cube.set_color(1, 0, 0, 1.0)
        
        the_ball = Sphere((5, 0, -5), 0.5, slices=15, stacks=15)
        the_ball.set_color(0, 0, 1, 1.0)
        
        the_light = Light(
            position=(-1, 1, 1),
            ambient=(0.2, 0.3, 0.5),
            diffuse=(1, 1, 1),
            specular=(0.1, 0.1, 0.1),
        )
        
        the_line = Line((-1, -1, -1), (0, 0, -10))
        the_line.set_color(1, 0, 1, 1.0)
        
        the_cylinder = Cylinder((-5, 0, -3), 1, 3, sides=15)
        the_cylinder.set_color(0, 1, 0, 1.0)
        
        self.renderer.add_object(the_line)
        self.renderer.add_object(the_cube)
        self.renderer.add_object(the_light)
        self.renderer.add_object(the_ball)
        self.renderer.add_object(the_cylinder)
        self.renderer.set_camera(self.camera)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.close()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.window.close()

    def process_input(self):
        keys = pygame.key.get_pressed()
        delta_time = self.clock.get_time() / 1000.0
        
        if keys[pygame.K_w]:
            self.camera.process_keyboard("FORWARD", delta_time)
        if keys[pygame.K_s]:
            self.camera.process_keyboard("BACKWARD", delta_time)
        if keys[pygame.K_a]:
            self.camera.process_keyboard("LEFT", delta_time)
        if keys[pygame.K_d]:
            self.camera.process_keyboard("RIGHT", delta_time)
        if keys[pygame.K_q]:
            self.camera.process_keyboard("UP", delta_time)
        if keys[pygame.K_e]:
            self.camera.process_keyboard("DOWN", delta_time)

        x, y = pygame.mouse.get_rel()
        self.camera.process_mouse_movement(x, -y)

    def run(self):
        while self.window.wait_for_close():
            self.handle_events()
            self.process_input()

            self.window.clear()
            glLoadIdentity()
            self.camera.get_view_matrix()

            self.renderer.render()
            self.window.update()

            self.clock.tick(60)
        
        pygame.quit()

def main():
    app = Application()
    app.run()

if __name__ == "__main__":
    main()
