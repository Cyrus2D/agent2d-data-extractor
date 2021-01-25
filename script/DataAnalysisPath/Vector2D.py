from AngleDeg import AngleDeg, EPSILON, DEG2RAD
import math


class Vector2D:  # TODO maybe give some bugs because of x and _x and x()

    def __init__(self,
                 x: float = None,
                 y: float = None,
                 vector2d=None):
        if x is not None and y is not None:
            self._x = x
            self._y = y
        elif vector2d is not None:
            self._x = vector2d._x
            self._y = vector2d._y
        else:
            self._x = 0
            self._y = 0
        self._is_valid = True

    def assign(self, __x, __y):
        self._x = __x
        self._y = __y
        return self

    def x(self):
        return self._x

    def y(self):
        return self._y

    def set_polar(self, __r, __d):
        if type(__d) is not AngleDeg:
            __d = AngleDeg(__d)
        self._x = __r * __d.cos()
        self._y = __r * __d.sin()

    def invalidate(self):
        self._is_valid = False

    def is_valid(self):
        return self._is_valid

    def r2(self):
        return self._x * self._x + self._y * self._y

    def r(self):
        return math.sqrt(self.r2())

    def length(self):
        return self.r()

    def length2(self):
        return self.r2()

    def th(self):
        return AngleDeg(AngleDeg.atan2_deg(self._y, self._x))

    def dir(self):
        return self.th()

    def abs(self):
        return Vector2D(abs(self._x), abs(self._y))

    def absX(self):
        return math.fabs(self._x)

    def absY(self):
        return math.fabs(self._y)

    def add(self, *args):  # **kwargs):
        if len(args) == 1:
            self._x += args[0].x()
            self._y += args[0].y()
        elif len(args) == 2:
            self._x += args[0]
            self._y += args[1]

    def scale(self, scalar):
        self._x *= scalar
        self._y *= scalar

    def __add__(self, other):
        return Vector2D(self._x + other.x(), self._y + other.y())

    def __sub__(self, other):
        return Vector2D(self._x - other._x, self._y - other._y)

    def __truediv__(self, other):
        return Vector2D(self._x / other, self._y / other)

    def __mul__(self, other):
        return Vector2D(self._x * other, self._y * other)

    def __iadd__(self, other):
        self._x += other.x()
        self._y += other.y()
        return self

    def __isub__(self, other):
        self._x -= other.x()
        self._y -= other.y()
        return self

    def __imul__(self, other):
        self._x *= other
        self._y *= other
        return self

    def __idiv__(self, other):
        self._x /= other
        self._y /= other
        return self

    def add_x(self, x: float):
        self._x += x

    def add_y(self, y: float):
        self._y += y

    def sub_x(self, x: float):
        self._x -= x

    def sub_y(self, y: float):
        self._y -= y

    def dist2(self, other):
        return math.pow(self._x - other.x(), 2) + math.pow(self._y - other.y(), 2)

    def dist(self, other):
        return math.sqrt(self.dist2(other))

    def reverse(self):
        self._x *= (-1.0)
        self._y *= (-1.0)

    def reverse_vector(self):
        new_vector = Vector2D(self._x, self._y)
        new_vector.reverse()
        return new_vector

    def set_length(self, length):
        mag = self.r()
        if mag > EPSILON:
            self.scale(length / mag)

    def set_length_vector(self, length):
        new_vector = Vector2D(self._x, self._y)
        new_vector.set_length(length)
        return new_vector

    def normalize(self):
        self.set_length(1)

    def normalize_vector(self):
        new_vector = Vector2D(self._x, self._y)
        new_vector.set_length(1)
        return new_vector

    def innerProduct(self, v):
        return self._x * v.x() + self._y * v.y()
        # ==  |this| * |v| * (*this - v).th().cos()

    def outerProduct(self, v):
        #   xn = self.y * v.z - self.z * v.y;
        #   yn = self.z * v.x - self.x * v.z;
        #   zn = self.x * v.y - self.y * v.x;
        return self._x * v._y - self._y * v._x
        # == |this| * |v| * (*this - v).th().sin()

    def equals(self, other):
        return self._x == other.x() and self._y == other.y()

    def equalsWeakly(self, other):
        return math.fabs(self._x - other.x) < EPSILON and math.fabs(self._y - other.y) < EPSILON

    def rotate(self, deg):
        if type(deg) == AngleDeg:
            self.rotate(deg.degree())
            return self
        cos_tmp = math.cos(deg * DEG2RAD)
        sin_tmp = math.sin(deg * DEG2RAD)
        self.assign(self._x * cos_tmp - self._y * sin_tmp, self._x * sin_tmp + self._y * cos_tmp)
        return self

    def rotated_vector(self, deg):
        new_vector = Vector2D(self._x, self._y)
        return new_vector.rotate(deg)

    def set_dir(self, direction):
        radius = self.r()
        self._x = radius * direction.cos()
        self._y = radius * direction.sin()

    @staticmethod
    def invalid():
        vec_invalid = Vector2D()
        vec_invalid.invalidate()
        return vec_invalid

    @staticmethod
    def from_polar(mag, theta):
        return Vector2D(mag * theta.cos(), mag * theta.sin())

    @staticmethod
    def polar2vector(__r, __d):
        new_vector = Vector2D()
        new_vector.set_polar(__r, __d)
        return new_vector

    @staticmethod
    def inner_product(v1, v2):
        return v1.innerProduct(v2)

    @staticmethod
    def outer_product(v1, v2):
        return v1.outerProduct(v2)

    def __repr__(self):
        return "({},{})".format(self._x, self._y)

    def copy(self):
        return Vector2D(self._x, self._y)
