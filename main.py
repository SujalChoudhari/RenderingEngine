import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from src.window import Window
from src.renderer import Renderer
from src.maths.vector import Vec3
from src.geometry.line import Line
from src.geometry.cube import Cube
from src.geometry.light import Light
from src.free_camera import FreeCamera


def main():
    pygame.init()
    window = Window(800, 600, "Hello World")
    renderer = Renderer()

    the_cube = Cube(Vec3(-0.5, -0.5, -5), Vec3(1, 1, 1))

    # Create LightGeometry instead of Light
    the_light = Light(
        position=(-1, 1, 1),
        ambient=(0.9, 0.9, 0.5),
        diffuse=(1, 1, 1),
        specular=(0.1, 0.1, 0.1),
    )

    camera = FreeCamera([0, 0, 3], [0, 0, -1], [0, 1, 0])

    renderer.add_object(Line(Vec3(-1, -1, -1), Vec3(0, 0, -10)))
    renderer.add_object(the_cube)
    renderer.add_object(the_light)  # Add the_light as an object to render
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    clock = pygame.time.Clock()

    while window.wait_for_close():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.close()
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                window.close()
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            camera.process_keyboard("FORWARD", clock.get_time() / 1000.0)
        if keys[pygame.K_s]:
            camera.process_keyboard("BACKWARD", clock.get_time() / 1000.0)
        if keys[pygame.K_a]:
            camera.process_keyboard("LEFT", clock.get_time() / 1000.0)
        if keys[pygame.K_d]:
            camera.process_keyboard("RIGHT", clock.get_time() / 1000.0)
        if keys[pygame.K_q]:
            camera.process_keyboard("UP", clock.get_time() / 1000.0)
        if keys[pygame.K_e]:
            camera.process_keyboard("DOWN", clock.get_time() / 1000.0)

        # Get mouse movement
        x, y = pygame.mouse.get_rel()
        camera.process_mouse_movement(x, -y)

        window.clear()
        glLoadIdentity()
        camera.get_view_matrix()

        renderer.render()
        window.update()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
