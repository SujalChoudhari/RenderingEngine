import numpy as np
import imgui
from imgui.integrations.pygame import PygameRenderer
from src.geometry.line import Line
from src.geometry.cube import Cube
from src.geometry.sphere import Sphere
from src.geometry.cylinder import Cylinder
from src.geometry.light import Light
from src.geometry.curve import Curve, BezierCurve, BSplineCurve


class ImGuiHandler:
    def __init__(self, window, objects):
        imgui.create_context()
        self.imgui_renderer = PygameRenderer()
        self.window = window
        self.objects = objects

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

                if hasattr(obj, "control_points"):
                    list_vertices = obj.control_points
                    for i, vertex in enumerate(list_vertices):
                        changed, new_vertex = imgui.input_float3(
                            f"Points {i+1}", *vertex
                        )
                        if changed:
                            list_vertices[i] = new_vertex
                    obj.control_points = list_vertices

                if hasattr(obj, "num_segments"):
                    num_segments = obj.num_segments
                    changed, new_num_segments = imgui.input_int(
                        "Number of Segments", num_segments
                    )
                    if changed:
                        obj.num_segments = new_num_segments

                if type(obj) is Sphere:
                    slices, stacks = obj.slices, obj.stacks
                    changed1, new_slices = imgui.input_int("Slices", slices)
                    changed2, new_stacks = imgui.input_int("Stacks", stacks)
                    if changed1:
                        obj.slices = new_slices
                    if changed2:
                        obj.stacks = new_stacks

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
