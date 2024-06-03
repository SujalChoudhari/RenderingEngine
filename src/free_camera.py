import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import numpy as np

class FreeCamera:
    def __init__(self, position, look_at, up):
        self.position = np.array(position, dtype=np.float32)
        self.look_at = np.array(look_at, dtype=np.float32)
        self.up = np.array(up, dtype=np.float32)
        self.pitch = 0.0
        self.yaw = -90.0

        self.front = np.array([0.0, 0.0, -1.0], dtype=np.float32)
        self.right = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        self.world_up = np.array(up, dtype=np.float32)

        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = np.array([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        ], dtype=np.float32)

        self.front = front / np.linalg.norm(front)
        self.right = np.cross(self.front, self.world_up)
        self.right /= np.linalg.norm(self.right)
        self.up = np.cross(self.right, self.front)
        self.up /= np.linalg.norm(self.up)

    def get_view_matrix(self):
        return gluLookAt(
            self.position[0], self.position[1], self.position[2],
            self.position[0] + self.front[0], self.position[1] + self.front[1], self.position[2] + self.front[2],
            self.up[0], self.up[1], self.up[2]
        )

    def process_keyboard(self, direction, delta_time):
        velocity = 5.0 * delta_time
        if direction == 'FORWARD':
            self.position += self.front * velocity
        if direction == 'BACKWARD':
            self.position -= self.front * velocity
        if direction == 'LEFT':
            self.position -= self.right * velocity
        if direction == 'RIGHT':
            self.position += self.right * velocity
        if direction == 'UP':
            self.position += self.up * velocity
        if direction == 'DOWN':
            self.position -= self.up * velocity

    def process_mouse_movement(self, xoffset, yoffset, sensitivity=0.1):
        xoffset *= sensitivity
        yoffset *= sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0

        self.update_camera_vectors()

    def get_direction(self):
        return self.front