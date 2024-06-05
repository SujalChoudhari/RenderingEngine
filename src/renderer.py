from OpenGL.GL import *
from src.free_camera import FreeCamera
from src.geometry.light import Light
class Renderer:
    def __init__(self):
        self.objects = []
        self.lights = []
        self.camera :FreeCamera= None

    def set_camera(self, camera):
        self.camera = camera

    def add_object(self, obj):
        if type(obj) is Light:
            self.lights.append(obj)
        else:
            self.objects.append(obj)

    def update(self,delta_time):
        for obj in self.objects:
            obj.update(delta_time)

    def render(self):
        camera_direction = self.camera.get_direction()
        for light in self.lights:
            light.apply_color()
            light.render(camera_direction)

        for obj in self.objects:
            obj.apply_color()
            obj.render(camera_direction)

        for light in self.lights:
            light.disable()
