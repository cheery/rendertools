import math

GLMAT_EPSILON = 0.000001

class mat3(list):
    def __init__(self):
        list.__init__(self)
        self[:] = [1.0, 0.0, 0.0,
                   0.0, 1.0, 0.0,
                   0.0, 0.0, 1.0]

    def clean(self, v=0.0):
        self[0] = self[1] = self[2] = v
        self[3] = self[4] = self[5] = v
        self[6] = self[7] = self[8] = v
        return self
    
    def from_mat4(self, a):
        self[0] = a[0]
        self[1] = a[1]
        self[2] = a[2]
        self[3] = a[4]
        self[4] = a[5]
        self[5] = a[6]
        self[6] = a[8]
        self[7] = a[9]
        self[8] = a[10]
        return self

    def clone(self):
        out = vec3()
        out[0] = self[0]
        out[1] = self[1]
        out[2] = self[2]
        out[3] = self[3]
        out[4] = self[4]
        out[5] = self[5]
        out[6] = self[6]
        out[7] = self[7]
        out[8] = self[8]
        return out

    def copy(self, a):
        self[0] = a[0]
        self[1] = a[1]
        self[2] = a[2]
        self[3] = a[3]
        self[4] = a[4]
        self[5] = a[5]
        self[6] = a[6]
        self[7] = a[7]
        self[8] = a[8]
        return self

    def identity(self):
        self[0] = 1.0
        self[1] = 0.0
        self[2] = 0.0
        self[3] = 0.0
        self[4] = 1.0
        self[5] = 0.0
        self[6] = 0.0
        self[7] = 0.0
        self[8] = 1.0
        return self

    def transpose(self, a):
        if self is a:
            a01 = a[1]
            a02 = a[2]
            a12 = a[5]
            self[1] = a[3]
            self[2] = a[6]
            self[3] = a01
            self[5] = a[7]
            self[6] = a02
            self[7] = a12
        else:
            self[0] = a[0]
            self[1] = a[3]
            self[2] = a[6]
            self[3] = a[1]
            self[4] = a[4]
            self[5] = a[7]
            self[6] = a[2]
            self[7] = a[5]
            self[8] = a[8]
        return self

    def invert(self, a):
        a00 = a[0]; a01 = a[1]; a02 = a[2]
        a10 = a[3]; a11 = a[4]; a12 = a[5]
        a20 = a[6]; a21 = a[7]; a22 = a[8]

        b01 = a22 * a11 - a12 * a21
        b11 = -a22 * a10 + a12 * a20
        b21 = a21 * a10 - a11 * a20

        det = a00 * b01 + a01 * b11 + a02 * b21

        if det == 0.0:
            return None
        det = 1.0 / det

        self[0] = b01 * det
        self[1] = (-a22 * a01 + a02 * a21) * det
        self[2] = (a12 * a01 - a02 * a11) * det
        self[3] = b11 * det
        self[4] = (a22 * a00 - a02 * a20) * det
        self[5] = (-a12 * a00 + a02 * a10) * det
        self[6] = b21 * det
        self[7] = (-a21 * a00 + a01 * a20) * det
        self[8] = (a11 * a00 - a01 * a10) * det
        return self

    def adjoint(self, a):
        a00 = a[0]; a01 = a[1]; a02 = a[2]
        a10 = a[3]; a11 = a[4]; a12 = a[5]
        a20 = a[6]; a21 = a[7]; a22 = a[8]

        out[0] = (a11 * a22 - a12 * a21)
        out[1] = (a02 * a21 - a01 * a22)
        out[2] = (a01 * a12 - a02 * a11)
        out[3] = (a12 * a20 - a10 * a22)
        out[4] = (a00 * a22 - a02 * a20)
        out[5] = (a02 * a10 - a00 * a12)
        out[6] = (a10 * a21 - a11 * a20)
        out[7] = (a01 * a20 - a00 * a21)
        out[8] = (a00 * a11 - a01 * a10)
        return out

    def determinant(a):
        a00 = a[0]; a01 = a[1]; a02 = a[2]
        a10 = a[3]; a11 = a[4]; a12 = a[5]
        a20 = a[6]; a21 = a[7]; a22 = a[8]
        return a00 * (a22 * a11 - a12 * a21) + a01 * (-a22 * a10 + a12 * a20) + a02 * (a21 * a10 - a11 * a20)

    def multiply(out, a, b):
        a00 = a[0]; a01 = a[1]; a02 = a[2]
        a10 = a[3]; a11 = a[4]; a12 = a[5]
        a20 = a[6]; a21 = a[7]; a22 = a[8]

        b00 = b[0]; b01 = b[1]; b02 = b[2]
        b10 = b[3]; b11 = b[4]; b12 = b[5]
        b20 = b[6]; b21 = b[7]; b22 = b[8]

        self[0] = b00 * a00 + b01 * a10 + b02 * a20
        self[1] = b00 * a01 + b01 * a11 + b02 * a21
        self[2] = b00 * a02 + b01 * a12 + b02 * a22

        self[3] = b10 * a00 + b11 * a10 + b12 * a20
        self[4] = b10 * a01 + b11 * a11 + b12 * a21
        self[5] = b10 * a02 + b11 * a12 + b12 * a22

        self[6] = b20 * a00 + b21 * a10 + b22 * a20
        self[7] = b20 * a01 + b21 * a11 + b22 * a21
        self[8] = b20 * a02 + b21 * a12 + b22 * a22
        return self

    def translate(self, a, v):
        a00 = a[0]; a01 = a[1]; a02 = a[2]
        a10 = a[3]; a11 = a[4]; a12 = a[5]
        a20 = a[6]; a21 = a[7]; a22 = a[8]
        x = v[0]; y = v[1]

        self[0] = a00
        self[1] = a01
        self[2] = a02

        self[3] = a10
        self[4] = a11
        self[5] = a12

        self[6] = x * a00 + y * a10 + a20
        self[7] = x * a01 + y * a11 + a21
        self[8] = x * a02 + y * a12 + a22
        return self

    def rotate(self, a, rad):
        a00 = a[0]; a01 = a[1]; a02 = a[2]
        a10 = a[3]; a11 = a[4]; a12 = a[5]
        a20 = a[6]; a21 = a[7]; a22 = a[8]

        s = math.sin(rad)
        c = math.cos(rad)

        self[0] = c * a00 + s * a10
        self[1] = c * a01 + s * a11
        self[2] = c * a02 + s * a12

        self[3] = c * a10 - s * a00
        self[4] = c * a11 - s * a01
        self[5] = c * a12 - s * a02

        self[6] = a20
        self[7] = a21
        self[8] = a22
        return self

    def rotate(self, a, rad, axis):
        x = axis[0]; y = axis[1]; z = axis[2]
        len = math.sqrt(x * x + y * y + z * z)

        if abs(len) < GLMAT_EPSILON:
            return None
        
        len = 1.0 / len
        x *= len
        y *= len
        z *= len

        s = math.sin(rad)
        c = math.cos(rad)
        t = 1.0 - c

        a00 = a[0]; a01 = a[1]; a02 = a[2];
        a10 = a[3]; a11 = a[4]; a12 = a[5];
        a20 = a[6]; a21 = a[7]; a22 = a[8];

        b00 = x * x * t + c; b01 = y * x * t + z * s; b02 = z * x * t - y * s
        b10 = x * y * t - z * s; b11 = y * y * t + c; b12 = z * y * t + x * s
        b20 = x * z * t + y * s; b21 = y * z * t - x * s; b22 = z * z * t + c

        self[0] = a00 * b00 + a10 * b01 + a20 * b02
        self[1] = a01 * b00 + a11 * b01 + a21 * b02
        self[2] = a02 * b00 + a12 * b01 + a22 * b02
        self[3] = a00 * b10 + a10 * b11 + a20 * b12
        self[4] = a01 * b10 + a11 * b11 + a21 * b12
        self[5] = a02 * b10 + a12 * b11 + a22 * b12
        self[6] = a00 * b20 + a10 * b21 + a20 * b22
        self[7] = a01 * b20 + a11 * b21 + a21 * b22
        self[8] = a02 * b20 + a12 * b21 + a22 * b22
    
        return self



    def scale(self, a, v):
        x = v[0]; y = v[1]

        self[0] = x * a[0]
        self[1] = x * a[1]
        self[2] = x * a[2]

        self[3] = y * a[3]
        self[4] = y * a[4]
        self[5] = y * a[5]

        self[6] = a[6]
        self[7] = a[7]
        self[8] = a[8]
        return self

    def from_mat2d(self, a):
        self[0] = a[0]
        self[1] = a[1]
        self[2] = 0.0

        self[3] = a[2]
        self[4] = a[3]
        self[5] = 0.0

        self[6] = a[4]
        self[7] = a[5]
        self[8] = 1.0
        return self

    def from_quat(self, q):
        x = q[0]; y = q[1]; z = q[2]; w = q[3]
        x2 = x + x
        y2 = y + y
        z2 = z + z

        xx = x * x2
        xy = x * y2
        xz = x * z2
        yy = y * y2
        yz = y * z2
        zz = z * z2
        wx = w * x2
        wy = w * y2
        wz = w * z2

        self[0] = 1.0 - (yy + zz)
        self[3] = xy + wz
        self[6] = xz - wy

        self[1] = xy - wz
        self[4] = 1.0 - (xx + zz)
        self[7] = yz + wx

        self[2] = xz + wy
        self[5] = yz - wx
        self[8] = 1.0 - (xx + yy)

        return self

    def normal_from_mat4(self, a):
        a00 = a[0]; a01 = a[1]; a02 = a[2]; a03 = a[3]
        a10 = a[4]; a11 = a[5]; a12 = a[6]; a13 = a[7]
        a20 = a[8]; a21 = a[9]; a22 = a[10]; a23 = a[11]
        a30 = a[12]; a31 = a[13]; a32 = a[14]; a33 = a[15]

        b00 = a00 * a11 - a01 * a10
        b01 = a00 * a12 - a02 * a10
        b02 = a00 * a13 - a03 * a10
        b03 = a01 * a12 - a02 * a11
        b04 = a01 * a13 - a03 * a11
        b05 = a02 * a13 - a03 * a12
        b06 = a20 * a31 - a21 * a30
        b07 = a20 * a32 - a22 * a30
        b08 = a20 * a33 - a23 * a30
        b09 = a21 * a32 - a22 * a31
        b10 = a21 * a33 - a23 * a31
        b11 = a22 * a33 - a23 * a32

        det = b00 * b11 - b01 * b10 + b02 * b09 + b03 * b08 - b04 * b07 + b05 * b06

        if det == 0.0:
            return None
        det = 1.0 / det

        self[0] = (a11 * b11 - a12 * b10 + a13 * b09) * det
        self[1] = (a12 * b08 - a10 * b11 - a13 * b07) * det
        self[2] = (a10 * b10 - a11 * b08 + a13 * b06) * det

        self[3] = (a02 * b10 - a01 * b11 - a03 * b09) * det
        self[4] = (a00 * b11 - a02 * b08 + a03 * b07) * det
        self[5] = (a01 * b08 - a00 * b10 - a03 * b06) * det

        self[6] = (a31 * b05 - a32 * b04 + a33 * b03) * det
        self[7] = (a32 * b02 - a30 * b05 - a33 * b01) * det
        self[8] = (a30 * b04 - a31 * b02 + a33 * b00) * det

        return self
