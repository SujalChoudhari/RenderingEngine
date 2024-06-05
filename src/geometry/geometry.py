from OpenGL.GL import *
import numpy as np

class Geometry:
    def __init__(
        self,
        position=(0.0, 0.0, 0.0),
        rotation=(0.0, 0.0, 0.0),
        color=(1.0, 1.0, 1.0, 1.0),
        keyframes=[],
        update_callback=None,
    ):
        self.update_callback = update_callback
        self.translation = np.array(position, dtype=np.float32)
        self.rotation = np.array(rotation, dtype=np.float32)
        self.color = np.array(color, dtype=np.float32)
        self.keyframes = keyframes
        self._current_keyframe = 0
        self._t = 0.0  # Interpolation parameter
        self._delta_time = 1.0  # Time interval to switch between keyframes

    def update(self, delta_time):
        if len(self.keyframes) < 2:
            return

        self._t += delta_time / self._delta_time

        if self._t >= 1.0:
            self._t = 0.0
            self._current_keyframe = (self._current_keyframe + 1) % len(self.keyframes)

        next_keyframe = (self._current_keyframe + 1) % len(self.keyframes)
        
        current_kf = self.keyframes[self._current_keyframe]
        next_kf = self.keyframes[next_keyframe]
        if 'position' in current_kf and 'position' in next_kf:
            self.translation = self.lerp_vector(current_kf['position'], next_kf['position'], self._t)
        if 'rotation' in current_kf and 'rotation' in next_kf:
            self.rotation = self.lerp_vector(current_kf['rotation'], next_kf['rotation'], self._t)
        if 'color' in current_kf and 'color' in next_kf:
            self.color = self.lerp_color(current_kf['color'], next_kf['color'], self._t)

        if self.update_callback:
            self.update_callback()

            
    def lerp(self, start, end, t):
        return start * (1.0 - t) + end * t

    def lerp_vector(self, start, end, t):
        new_x = self.lerp(start[0], end[0], t)
        new_y = self.lerp(start[1], end[1], t)
        new_z = self.lerp(start[2], end[2], t)
        return np.array([new_x, new_y, new_z])

    def lerp_color(self, start, end, t):
        new_r = self.lerp(start[0], end[0], t)
        new_g = self.lerp(start[1], end[1], t)
        new_b = self.lerp(start[2], end[2], t)
        new_a = self.lerp(start[3], end[3], t)
        return np.array([new_r, new_g, new_b, new_a])

    def translate(self, x, y, z):
        self.translation += np.array([x, y, z])

    def rotate(self, x, y, z):
        self.rotation += np.array([x, y, z])

    def change_color(self, r, g, b, a=1.0):
        self.color = np.array([r, g, b, a])

    def change_position(self, x, y, z):
        self.translation = np.array([x, y, z])

    def change_rotation(self, x, y, z):
        self.rotation = np.array([x, y, z])
        self.recalculate_normals()

    def recalculate_normals(self):
        pass

    def apply_transformations(self):
        glTranslatef(*self.translation)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)

    def apply_color(self):
        glColor4f(self.color[0], self.color[1], self.color[2], self.color[3])

    def is_face_visible(self, face_normal, camera_direction, buffer=0.1):
        dot_product = np.dot(face_normal, camera_direction)
        return dot_product <= buffer or True

    def get_rotation_matrix(self):
        angle = np.radians(self.rotation)
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)

        rx = np.array(
            [
                [1, 0, 0, 0],
                [0, cos_a[0], -sin_a[0], 0],
                [0, sin_a[0], cos_a[0], 0],
                [0, 0, 0, 1],
            ]
        )

        ry = np.array(
            [
                [cos_a[1], 0, sin_a[1], 0],
                [0, 1, 0, 0],
                [-sin_a[1], 0, cos_a[1], 0],
                [0, 0, 0, 1],
            ]
        )

        rz = np.array(
            [
                [cos_a[2], -sin_a[2], 0, 0],
                [sin_a[2], cos_a[2], 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )

        rotation_matrix = np.dot(np.dot(rz, ry), rx)
        return rotation_matrix

    def render(self, camera_direction):
        # Apply transformations
        self.apply_transformations()
        self.apply_color()
        # Add rendering logic here
        pass