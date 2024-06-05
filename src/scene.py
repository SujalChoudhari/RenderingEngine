import json

from src.geometry.line import Line
from src.geometry.cube import Cube
from src.geometry.sphere import Sphere
from src.geometry.cylinder import Cylinder
from src.geometry.light import Light
from src.geometry.curve import Curve, BezierCurve, BSplineCurve

class Scene:
    def __init__(self, app, scene_path):
        with open(scene_path, "r") as f:
            str_data = f.read()
            json_data = json.loads(str_data)

        self.init_objects = json_data["objects"]
        self.app = app
        self.objects = []
        self.lights = []
        self.sceneID = -1
        self.init()

    def init(self):
        self.objects = []
        self.lights = []
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
            elif obj["type"] == "curve":
                curve = Curve(
                    control_points=obj["control_points"],
                )
                self.objects.append(curve)
            elif obj["type"] == "bezier_curve":
                curve = BezierCurve(
                    control_points=obj["control_points"],
                    num_segments=obj.get("num_segments", 100),
                )
                self.objects.append(curve)
            elif obj["type"] == "bspline_curve":
                curve = BSplineCurve(
                    control_points=obj["control_points"],
                    degree=obj.get("degree", 3),
                    num_segments=obj.get("num_segments", 100),
                )
                self.objects.append(curve)
            elif obj["type"] == "light":
                light = Light(
                    position=obj["position"],
                    ambient=obj["ambient"],
                    diffuse=obj["diffuse"],
                    specular=obj["specular"],
                )
                self.lights.append(light)
                self.objects.append(light)  # Add light to objects list for UI rendering

            self.app.renderer.add_object(self.objects[-1])

