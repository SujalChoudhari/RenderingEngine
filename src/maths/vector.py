class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vec2(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vec2(self.x / other, self.y / other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def to_tuple(self):
        return (self.x, self.y)



class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Vec3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        return Vec3(self.x / other, self.y / other, self.z / other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def to_tuple(self):
        return (self.x, self.y, self.z)

