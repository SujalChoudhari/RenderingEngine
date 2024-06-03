import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import imgui
from imgui.integrations.pygame import PygameRenderer
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
        
        # Initialize object_positions before calling initialize_objects
        self.object_positions = {
            "Cube": [-0.5, -0.5, -5],
            "Sphere": [5, 0, -5],
            "Cylinder": [-5, 0, -3],
            "Light": [0, 0, 0],
        }

        self.initialize_objects()
        
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        self.mouse_locked = True  # Track mouse lock state
        
        imgui.create_context()
        self.imgui_renderer = PygameRenderer()

        self.selected_object = None

    def initialize_objects(self):
        self.the_cube = Cube(self.object_positions["Cube"], (1, 1, 1))
        self.the_cube.set_color(1, 0, 0, 1.0)
        
        self.the_ball = Sphere(self.object_positions["Sphere"], 0.5, slices=15, stacks=15)
        self.the_ball.set_color(0, 0, 1, 1.0)
        
        self.the_cylinder = Cylinder(self.object_positions["Cylinder"], 1, 3, sides=15)
        self.the_cylinder.set_color(0, 1, 0, 1.0)

        self.the_light = Light(
            position=self.object_positions["Light"],
            ambient=(0.2, 0.3, 0.5),
            diffuse=(1, 1, 1),
            specular=(0.1, 0.1, 0.1),
        )

        self.renderer.add_object(self.the_cube)
        self.renderer.add_object(self.the_ball)
        self.renderer.add_object(self.the_cylinder)
        self.renderer.add_object(self.the_light)
        self.renderer.set_camera(self.camera)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.close()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.toggle_mouse_lock()
            self.imgui_renderer.process_event(event)

    def toggle_mouse_lock(self):
        self.mouse_locked = not self.mouse_locked
        pygame.mouse.set_visible(not self.mouse_locked)
        pygame.event.set_grab(self.mouse_locked)

    def process_input(self):
        if self.mouse_locked:
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

    def show_ui(self):
        imgui.get_io().display_size = (self.window.width, self.window.height)
        imgui.new_frame()

        imgui.begin("Object Controls")
        for name, position in self.object_positions.items():
            if imgui.tree_node(name):
                changed, value = imgui.input_float3("Position", *position)
                if changed:
                    self.object_positions[name] = value
                    if name == "Cube":
                        self.the_cube.change_position(value)
                    elif name == "Sphere":
                        self.the_ball.change_position(value)
                    elif name == "Cylinder":
                        self.the_cylinder.change_position(value)
                    elif name == "Light":
                        self.the_light.change_position(value)
                imgui.tree_pop()
        imgui.end()

        imgui.render()
        self.imgui_renderer.render(imgui.get_draw_data())

    def run(self):
        while self.window.wait_for_close():
            self.window.clear()
            self.handle_events()
            self.process_input()
            glLoadIdentity()
            self.camera.get_view_matrix()
            self.renderer.render()
            self.show_ui()
            self.window.update()
            self.clock.tick(60)
        
        pygame.quit()

def main():
    app = Application()
    app.run()

if __name__ == "__main__":
    main()