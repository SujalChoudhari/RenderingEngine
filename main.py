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
from src.app.app import Application


def main():
    objects = {
        "line": {"type": "line", "origin": (0, 0, 0), "destination": (1, 1, 1)},
        "cube": {"type": "cube", "position": (0, 0, 0), "size": (1, 1, 1)},
        "light": {
            "type": "light",
            "position": (-10, 10, 10),
            "ambient": (.4, .4, .3),
            "diffuse": (1, 1, 1),
            "specular": (0.1, 0.1, 0.1),
        },
    }
    app = Application()
    app.initialize_objects(objects)
    app.run()


if __name__ == "__main__":
    main()
