from OpenGL.GL import *

class Renderer:
    def __init__(self):
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def render(self):
        for obj in self.objects:
            obj.apply_color()
            obj.update()
            obj.render()
