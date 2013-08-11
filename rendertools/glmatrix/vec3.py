import math, random

class vec3(list):
    def __init__(self):
        list.__init__(self)
        self[:] = [0.0, 0.0, 0.0]

    def clone(self):
        out = vec3()
        out[0] = self[0]
        out[1] = self[1]
        out[2] = self[2]
        return out

    @classmethod
    def from_values(cls, x, y, z):
        out = cls()
        out[0] = x
        out[1] = y
        out[2] = z
        return out

    def copy(self, a):
        self[0] = a[0]
        self[1] = a[1]
        self[2] = a[2]
        return self

    def add(self, a, b):
        self[0] = a[0] + b[0]
        self[1] = a[1] + b[1]
        self[2] = a[2] + b[2]
        return self

    def subtract(self, a, b):
        self[0] = a[0] - b[0]
        self[1] = a[1] - b[1]
        self[2] = a[2] - b[2]
        return self

    def multiply(self, a, b):
        self[0] = a[0] * b[0]
        self[1] = a[1] * b[1]
        self[2] = a[2] * b[2]
        return self

    def divide(self, a, b):
        self[0] = a[0] / b[0]
        self[1] = a[1] / b[1]
        self[2] = a[2] / b[2]
        return self

    def min(self, a, b):
        self[0] = math.min(a[0], b[0])
        self[1] = math.min(a[1], b[1])
        self[2] = math.min(a[2], b[2])
        self[3] = math.min(a[3], b[3])
        return self

    def max(self, a, b):
        self[0] = math.max(a[0], b[0])
        self[1] = math.max(a[1], b[1])
        self[2] = math.max(a[2], b[2])
        return self

    def scale(self, a, b):
        self[0] = a[0] * b
        self[1] = a[1] * b
        self[2] = a[2] * b
        return self

    def scale_and_add(self, a, b, scale):
        self[0] = a[0] + (b[0] * scale)
        self[1] = a[1] + (b[1] * scale)
        self[2] = a[2] + (b[2] * scale)
        return self

    def distance(self, b):
        x = b[0] - self[0]
        y = b[1] - self[1]
        z = b[2] - self[2]
        return math.sqrt(x*x + y*y + z*z)

    def squared_distance(self, b):
        x = b[0] - self[0]
        y = b[1] - self[1]
        z = b[2] - self[2]
        return x*x + y*y + z*z

    def length(self):
        x = self[0]
        y = self[1]
        z = self[2]
        return math.sqrt(x*x + y*y + z*z)
        
    def squared_length(self):
        x = self[0]
        y = self[1]
        z = self[2]
        return x*x + y*y + z*z

    def negate(self, a):
        self[0] = -a[0]
        self[1] = -a[1]
        self[2] = -a[2]
        return self

    def normalize(self, a):
        x = a[0]
        y = a[1]
        z = a[2]
        len = x*x + y*y + z*z
        if len > 0.0:
            len = 1.0 / math.sqrt(len)
            self[0] = a[0] * len
            self[1] = a[1] * len
            self[2] = a[2] * len
        return self

    def dot(self, b):
        return self[0] * b[0] + self[1] * b[1] + self[2] * b[2]

    def cross(self, a, b):
        ax = a[0]; ay = a[1]; az = a[2]
        bx = b[0]; by = b[1]; bz = b[2]

        self[0] = ay * bz - az * by
        self[1] = az * bx - ax * bz
        self[2] = ax * by - ay * bx
        return self

    def lerp(self, a, b, t):
        ax = a[0]
        ay = a[1]
        az = a[2]
        self[0] = ax + t * (b[0] - ax)
        self[1] = ay + t * (b[1] - ay)
        self[2] = az + t * (b[2] - az)
        return self

    def random(self, scale=1.0):
        self[0] = random.random()
        self[1] = random.random()
        self[2] = random.random()
        self.normalize(self)
        if scale != 1.0:
            self.scale(self, self, scale)
        return self

    def transform_mat4(self, a, m):
        x = a[0]; y = a[1]; z = a[2]
        self[0] = m[0] * x + m[4] * y + m[8] * z + m[12]
        self[1] = m[1] * x + m[5] * y + m[9] * z + m[13]
        self[2] = m[2] * x + m[6] * y + m[10] * z + m[14]
        return self

    def transform_mat3(self, a, m):
        x = a[0]; y = a[1]; z = a[2]
        self[0] = x * m[0] + y * m[3] + z * m[6]
        self[1] = x * m[1] + y * m[4] + z * m[7]
        self[2] = x * m[2] + y * m[5] + z * m[8]
        return self
    
    def transform_quat(self, a, q):
        x = a[0]; y = a[1]; z = a[2]
        qx = q[0]; qy = q[1]; qz = q[2]; qw = q[3]

        ix = qw * x + qy * z - qz * y,
        iy = qw * y + qz * x - qx * z,
        iz = qw * z + qx * y - qy * x,
        iw = -qx * x - qy * y - qz * z

        self[0] = ix * qw + iw * -qx + iy * -qz - iz * -qy
        self[1] = iy * qw + iw * -qy + iz * -qx - ix * -qz
        self[2] = iz * qw + iw * -qz + ix * -qy - iy * -qx
        return self
