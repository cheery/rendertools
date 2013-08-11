import math
from vec3 import vec3
from vec4 import vec4
from mat3 import mat3

tmpvec3 = vec3()
xUnitVec3 = vec3.from_values(1.0,0.0,0.0)
yUnitVec3 = vec3.from_values(0.0,1.0,0.0)
tmpmat3 = mat3()

class quat(list):
    def __init__(self):
        list.__init__(self)
        self[:] = [0.0, 0.0, 0.0, 1.0]

    def rotation_to(self, a, b):
        dot = a.dot(b)
        if dot < -0.999999:
            tmpvec3.cross(xUnitVec3, a)
            if tmpvec3.length() < 0.000001:
                tmpvec3.cross(yUnitVec3, a)
            tmpvec3.normalize(tmpvec3)
            quat.set_axis_angle(self, tmpvec3, math.PI)
            return self
        elif dot > 0.999999:
            self[0] = 0.0
            self[1] = 0.0
            self[2] = 0.0
            self[3] = 1.0
            return self
        else:
            tmpvec3.cross(a, b)
            self[0] = tmpvec3[0]
            self[1] = tmpvec3[1]
            self[2] = tmpvec3[2]
            self[3] = 1.0 + dot
            return self.normalize(self)

    def set_axes(self, view, right, up):
        tmpmat3[0] = right[0]
        tmpmat3[3] = right[1]
        tmpmat3[6] = right[2]

        tmpmat3[1] = up[0]
        tmpmat3[4] = up[1]
        tmpmat3[7] = up[2]

        tmpmat3[2] = view[0]
        tmpmat3[5] = view[1]
        tmpmat3[8] = view[2]
        return self.normalize(self, self.from_mat3(tmpmat3))

    def clone(self):
        out = quat()
        out[0] = self[0]
        out[1] = self[1]
        out[2] = self[2]
        out[3] = self[3]
        return out

    @classmethod
    def from_values(cls, x, y, z, w):
        out = cls()
        out[0] = x
        out[1] = y
        out[2] = z
        out[3] = w
        return out

    def copy(self, a):
        self[0] = a[0]
        self[1] = a[1]
        self[2] = a[2]
        self[3] = a[3]
        return self

    def identity(self):
        self[0] = 0.0
        self[1] = 0.0
        self[2] = 0.0
        self[3] = 1.0
        return self
    
    def set_axis_angle(self, axis, rad):
        rad = rad * 0.5
        s = math.sin(rad)
        self[0] = s * axis[0]
        self[1] = s * axis[1]
        self[2] = s * axis[2]
        self[3] = math.cos(rad)
        return self

    def add(self, a, b):
        self[0] = a[0] + b[0]
        self[1] = a[1] + b[1]
        self[2] = a[2] + b[2]
        self[3] = a[3] + b[3]
        return self

    def multiply(self, a, b):
        ax = a[0]; ay = a[1]; az = a[2]; aw = a[3]
        bx = b[0]; by = b[1]; bz = b[2]; bw = b[3]

        self[0] = ax * bw + aw * bx + ay * bz - az * by
        self[1] = ay * bw + aw * by + az * bx - ax * bz
        self[2] = az * bw + aw * bz + ax * by - ay * bx
        self[3] = aw * bw - ax * bx - ay * by - az * bz
        return self

    def scale(self, a, b):
        self[0] = a[0] * b
        self[1] = a[1] * b
        self[2] = a[2] * b
        self[3] = a[3] * b
        return self

    def calculate_w(self, a):
        x = a[0]; y = a[1]; z = a[2]
        self[0] = x
        self[1] = y
        self[2] = z
        self[3] = -math.sqrt(math.abs(1.0 - x * x - y * y - z * z))
        return self

    def dot(self, b):
        return self[0] * b[0] + self[1] * b[1] + self[2] * b[2] + self[3] * b[3]

    def lerp(self, a, b, t):
        ax = a[0]
        ay = a[1]
        az = a[2]
        aw = a[3]
        self[0] = ax + t * (b[0] - ax)
        self[1] = ay + t * (b[1] - ay)
        self[2] = az + t * (b[2] - az)
        self[3] = aw + t * (b[3] - aw)
        return self

    def slerp(self, a, b, t):
        ax = a[0]; ay = a[1]; az = a[2]; aw = a[3]
        bx = b[0]; by = b[1]; bz = b[2]; bw = b[3]
        cosom = ax * bx + ay * by + az * bz + aw * bw
        if cosom < 0.0:
            cosom = -cosom
            bx = - bx
            by = - by
            bz = - bz
            bw = - bw
        if (1.0 - cosom) > 0.000001:
            omega  = math.acos(cosom)
            sinom  = math.sin(omega)
            scale0 = math.sin((1.0 - t) * omega) / sinom
            scale1 = math.sin(t * omega) / sinom
        else:
            scale0 = 1.0 - t
            scale1 = t
        self[0] = scale0 * ax + scale1 * bx
        self[1] = scale0 * ay + scale1 * by
        self[2] = scale0 * az + scale1 * bz
        self[3] = scale0 * aw + scale1 * bw
        return self

    def invert(self, a):
        a0 = a[0]; a1 = a[1]; a2 = a[2]; a3 = a[3]
        dot = a0*a0 + a1*a1 + a2*a2 + a3*a3
        invDot = 1.0/dot if dot else 0.0

        self[0] = -a0*invDot
        self[1] = -a1*invDot
        self[2] = -a2*invDot
        self[3] = a3*invDot
        return self

    def conjugate(self, a):
        self[0] = -a[0]
        self[1] = -a[1]
        self[2] = -a[2]
        self[3] = a[3]
        return self

    def length(self):
        x = self[0]
        y = self[1]
        z = self[2]
        w = self[3]
        return math.sqrt(x*x + y*y + z*z + w*w)
        
    def squared_length(self):
        x = self[0]
        y = self[1]
        z = self[2]
        w = self[3]
        return x*x + y*y + z*z + w*w

    def normalize(self, a):
        x = a[0]
        y = a[1]
        z = a[2]
        w = a[3]
        len = x*x + y*y + z*z + w*w
        if len > 0.0:
            len = 1.0 / math.sqrt(len)
            self[0] = a[0] * len
            self[1] = a[1] * len
            self[2] = a[2] * len
            self[3] = a[3] * len
        return self

    def from_mat3(self, m):
        fTrace = m[0] + m[4] + m[8]

        if fTrace > 0.0:
            fRoot = math.sqrt(fTrace + 1.0)
            self[3] = 0.5 * fRoot
            fRoot = 0.5/fRoot
            self[0] = (m[7]-m[5])*fRoot
            self[1] = (m[2]-m[6])*fRoot
            self[2] = (m[3]-m[1])*fRoot
        else:
            i = 0
            if m[4] > m[0]:
                i = 1
            if m[8] > m[i*3+i]:
                i = 2
                j = (i+1)%3
                k = (i+2)%3
            fRoot = math.sqrt(m[i*3+i]-m[j*3+j]-m[k*3+k] + 1.0)
            self[i] = 0.5 * fRoot
            fRoot = 0.5 / fRoot
            self[3] = (m[k*3+j] - m[j*3+k]) * fRoot
            self[j] = (m[j*3+i] + m[i*3+j]) * fRoot
            self[k] = (m[k*3+i] + m[i*3+k]) * fRoot
        return self
