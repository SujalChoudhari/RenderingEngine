import numpy as np
import imgui
from imgui.integrations.pygame import PygameRenderer
from src.geometry.line import Line
from src.geometry.cube import Cube
from src.geometry.sphere import Sphere
from src.geometry.cylinder import Cylinder
from src.geometry.light import Light


class ImGuiHandler:
    def __init__(self, window, renderer, init_objects=dict):
        imgui.create_context()
        self.imgui_renderer = PygameRenderer()
        self.renderer = renderer
        self.window = window
        self.objects = []
        self.lights = []
        self.init_objects = init_objects if init_objects is not None else []

        self.create_objects()

    def create_objects(self):
        for key, obj in self.init_objects.items():
            print(key, obj)
            if obj["type"] == "line":
                line = Line(obj["origin"], obj["destination"])
                self.objects.append(line)
            elif obj["type"] == "cube":
                cube = Cube(obj["position"], obj.get("size", (1, 1, 1)))
                cube.change_color(*obj.get("color", (1, 1, 1, 1)))
                self.objects.append(cube)
            elif obj["type"] == "sphere":
                sphere = Sphere(obj["position"], obj["radius"], slices=15, stacks=15)
                sphere.change_color(*obj.get("color", (1, 1, 1, 1)))
                self.objects.append(sphere)
            elif obj["type"] == "cylinder":
                cylinder = Cylinder(
                    obj["position"], obj["radius"], obj["height"], sides=15
                )
                cylinder.change_color(*obj.get("color", (1, 1, 1, 1)))
                self.objects.append(cylinder)
            elif obj["type"] == "light":
                light = Light(
                    position=obj["position"],
                    ambient=obj["ambient"],
                    diffuse=obj["diffuse"],
                    specular=obj["specular"],
                )
                self.lights.append(light)
                self.objects.append(light)  # Add light to objects list for UI rendering

            self.renderer.add_object(self.objects[-1])

    def render_transforms(self):
        imgui.begin("Objects")
        for obj in self.objects:
            obj_name = obj.__class__.__name__
            if imgui.tree_node(obj_name):
                position = list(obj.translation)
                changed, new_position = imgui.input_float3("Position", *position)
                if changed:
                    obj.change_position(
                        new_position[0], new_position[1], new_position[2]
                    )

                if hasattr(obj, "color") and type(obj) is not Light:
                    color = list(obj.color)
                    changed, new_color = imgui.color_edit4("Color", *color)
                    if changed:
                        obj.change_color(*new_color)
                if hasattr(obj, "ambient") and type(obj) is Light:
                    ambient = list(obj.ambient)
                    diffuse = list(obj.diffuse)
                    specular = list(obj.specular)
                    changed1, new_ambient = imgui.color_edit3("Ambient", *ambient)
                    changed2, new_diffuse = imgui.input_float3("Diffuse", *diffuse)
                    changed3, new_specular = imgui.input_float3("Specular", *specular)
                    if changed1 or changed2 or changed3:
                        obj.change_color(new_ambient, new_diffuse, new_specular)
                if hasattr(obj, "rotation"):
                    rotation = list(obj.rotation)
                    changed, new_rotation = imgui.input_float3("Rotation", *rotation)
                    if changed:
                        obj.change_rotation(
                            new_rotation[0], new_rotation[1], new_rotation[2]
                        )
                # Add more UI controls for other properties as needed
                imgui.tree_pop()
        imgui.end()

    def handle_event(self, event):
        self.imgui_renderer.process_event(event)

    def render_ui(self):
        imgui.get_io().display_size = (self.window.width, self.window.height)
        imgui.new_frame()
        self.render_transforms()
        imgui.render()
        self.imgui_renderer.render(imgui.get_draw_data())
