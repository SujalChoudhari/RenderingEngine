
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

from src.geometry.geometry import Geometry

class Curve(Geometry):
    def __init__(self, control_points, update=None):
        super().__init__(position=[0, 0, 0], update_callback=update)
        self.control_points = control_points

    def render(self, camera_position):
        self.apply_transformations()
        self.apply_color()
        glBegin(GL_LINE_STRIP)
        for vertex in self.control_points:
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()



class BezierCurve(Geometry):
    def __init__(self, control_points, num_segments=100, update=None):
        super().__init__(position=[0, 0, 0], update_callback=update)
        self.control_points = control_points
        self.num_segments = num_segments

    def calculate_bezier_point(self, t):
        p0, p1, p2, p3 = self.control_points
        return (
            (1-t)**3 * np.array(p0) +
            3 * (1-t)**2 * t * np.array(p1) +
            3 * (1-t) * t**2 * np.array(p2) +
            t**3 * np.array(p3)
        )

    def render(self, camera_position):
        self.apply_transformations()
        self.apply_color()
        glBegin(GL_LINE_STRIP)
        for i in range(self.num_segments + 1):
            t = i / self.num_segments
            point = self.calculate_bezier_point(t)
            glVertex3f(point[0], point[1], point[2])
        glEnd()


class BSplineCurve(Geometry):
    def __init__(self, control_points, degree=3, num_segments=100, update=None):
        super().__init__(position=[0, 0, 0], update_callback=update)
        self.control_points = control_points
        self.degree = degree
        self.num_segments = num_segments
        self.knot_vector = self.create_uniform_knot_vector(len(control_points), degree)

    def create_uniform_knot_vector(self, num_control_points, degree):
        n = num_control_points + degree + 1
        return [i for i in range(n)]

    def bspline_basis(self, i, k, t, knot_vector):
        if k == 0:
            return 1.0 if knot_vector[i] <= t < knot_vector[i + 1] else 0.0
        else:
            denom1 = knot_vector[i + k] - knot_vector[i]
            denom2 = knot_vector[i + k + 1] - knot_vector[i + 1]
            term1 = ((t - knot_vector[i]) / denom1 * self.bspline_basis(i, k - 1, t, knot_vector)) if denom1 != 0 else 0
            term2 = ((knot_vector[i + k + 1] - t) / denom2 * self.bspline_basis(i + 1, k - 1, t, knot_vector)) if denom2 != 0 else 0
            return term1 + term2

    def calculate_bspline_point(self, t):
        n = len(self.control_points) - 1
        point = np.zeros(3)
        for i in range(n + 1):
            basis = self.bspline_basis(i, self.degree, t, self.knot_vector)
            point += basis * np.array(self.control_points[i])
        return point

    def render(self, camera_position):
        self.apply_transformations()
        self.apply_color()
        glBegin(GL_LINE_STRIP)
        for i in range(self.num_segments + 1):
            t = (i / self.num_segments) * (self.knot_vector[-1] - self.degree)
            point = self.calculate_bspline_point(t)
            glVertex3f(point[0], point[1], point[2])
        glEnd()