from OpenGL.GL import *
from src.free_camera import FreeCamera
class Renderer:
    def __init__(self):
        self.objects = []
        self.camera :FreeCamera= None

    def set_camera(self, camera):
        self.camera = camera

    def add_object(self, obj):
        self.objects.append(obj)

    def render(self):
        camera_direction = self.camera.get_direction()
        for obj in self.objects:
            obj.apply_color()
            obj.update()
            obj.render(camera_direction)
