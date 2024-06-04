import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

from src.window import Window
from src.renderer import Renderer
from src.free_camera import FreeCamera
from src.app.imguihandler import ImGuiHandler

from src.window import Window
from src.renderer import Renderer


class Application:
    def __init__(self, width=800, height=600, title="Rendering Engine"):
        pygame.init()
        self.window = Window(width=width, height=height, title=title)
        self.renderer = Renderer()
        self.clock = pygame.time.Clock()
        self.camera = FreeCamera([0, 0, 3], [0, 0, -1], [0, 1, 0])
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        self.mouse_locked = True

    def initialize_objects(self, objects):
        self.renderer.set_camera(self.camera)
        self.imgui_handler = ImGuiHandler(self.window, self.renderer, objects)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.close()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.toggle_mouse_lock()
            self.imgui_handler.handle_event(event)

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

    def run(self):
        while self.window.wait_for_close():
            self.window.clear()
            self.handle_events()
            self.process_input()
            glLoadIdentity()
            self.camera.get_view_matrix()
            self.renderer.render()
            self.imgui_handler.render_ui()
            self.window.update()
            self.clock.tick(60)
        pygame.quit()
