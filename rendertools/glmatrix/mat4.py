import math

GLMAT_EPSILON = 0.000001

class mat4(list):
    def __init__(self):
        list.__init__(self)
        self[:] = [1.0, 0.0, 0.0, 0.0,
                   0.0, 1.0, 0.0, 0.0,
                   0.0, 0.0, 1.0, 0.0,
                   0.0, 0.0, 0.0, 1.0]

    def clean(self, v=0.0):
        self[0] = self[1] = self[2] = self[3] = v
        self[4] = self[5] = self[6] = self[7] = v
        self[8] = self[9] = self[10] = self[11] = v
        self[12] = self[13] = self[14] = self[15] = v
        return self

    def clone(a):
        out = mat4()
        out[0] = a[0]
        out[1] = a[1]
        out[2] = a[2]
        out[3] = a[3]
        out[4] = a[4]
        out[5] = a[5]
        out[6] = a[6]
        out[7] = a[7]
        out[8] = a[8]
        out[9] = a[9]
        out[10] = a[10]
        out[11] = a[11]
        out[12] = a[12]
        out[13] = a[13]
        out[14] = a[14]
        out[15] = a[15]
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
        self[9] = a[9]
        self[10] = a[10]
        self[11] = a[11]
        self[12] = a[12]
        self[13] = a[13]
        self[14] = a[14]
        self[15] = a[15]
        return self

    def identity(self):
        self[0] = 1.0
        self[1] = 0.0
        self[2] = 0.0
        self[3] = 0.0
        self[4] = 0.0
        self[5] = 1.0
        self[6] = 0.0
        self[7] = 0.0
        self[8] = 0.0
        self[9] = 0.0
        self[10] = 1.0
        self[11] = 0.0
        self[12] = 0.0
        self[13] = 0.0
        self[14] = 0.0
        self[15] = 1.0
        return self

    def transpose(self, a):
        if self is a:
            a01 = a[1]; a02 = a[2]; a03 = a[3]
            a12 = a[6]; a13 = a[7]
            a23 = a[11]

            self[1] = a[4]
            self[2] = a[8]
            self[3] = a[12]
            self[4] = a01
            self[6] = a[9]
            self[7] = a[13]
            self[8] = a02
            self[9] = a12
            self[11] = a[14]
            self[12] = a03
            self[13] = a13
            self[14] = a23
        else:
            self[0] = a[0]
            self[1] = a[4]
            self[2] = a[8]
            self[3] = a[12]
            self[4] = a[1]
            self[5] = a[5]
            self[6] = a[9]
            self[7] = a[13]
            self[8] = a[2]
            self[9] = a[6]
            self[10] = a[10]
            self[11] = a[14]
            self[12] = a[3]
            self[13] = a[7]
            self[14] = a[11]
            self[15] = a[15]
    
        return self

    def invert(self, a):
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
        self[1] = (a02 * b10 - a01 * b11 - a03 * b09) * det
        self[2] = (a31 * b05 - a32 * b04 + a33 * b03) * det
        self[3] = (a22 * b04 - a21 * b05 - a23 * b03) * det
        self[4] = (a12 * b08 - a10 * b11 - a13 * b07) * det
        self[5] = (a00 * b11 - a02 * b08 + a03 * b07) * det
        self[6] = (a32 * b02 - a30 * b05 - a33 * b01) * det
        self[7] = (a20 * b05 - a22 * b02 + a23 * b01) * det
        self[8] = (a10 * b10 - a11 * b08 + a13 * b06) * det
        self[9] = (a01 * b08 - a00 * b10 - a03 * b06) * det
        self[10] = (a30 * b04 - a31 * b02 + a33 * b00) * det
        self[11] = (a21 * b02 - a20 * b04 - a23 * b00) * det
        self[12] = (a11 * b07 - a10 * b09 - a12 * b06) * det
        self[13] = (a00 * b09 - a01 * b07 + a02 * b06) * det
        self[14] = (a31 * b01 - a30 * b03 - a32 * b00) * det
        self[15] = (a20 * b03 - a21 * b01 + a22 * b00) * det

        return self

    def adjoint(self, a):
        a00 = a[0]; a01 = a[1]; a02 = a[2]; a03 = a[3]
        a10 = a[4]; a11 = a[5]; a12 = a[6]; a13 = a[7]
        a20 = a[8]; a21 = a[9]; a22 = a[10]; a23 = a[11]
        a30 = a[12]; a31 = a[13]; a32 = a[14]; a33 = a[15]

        self[0]  =  (a11 * (a22 * a33 - a23 * a32) - a21 * (a12 * a33 - a13 * a32) + a31 * (a12 * a23 - a13 * a22))
        self[1]  = -(a01 * (a22 * a33 - a23 * a32) - a21 * (a02 * a33 - a03 * a32) + a31 * (a02 * a23 - a03 * a22))
        self[2]  =  (a01 * (a12 * a33 - a13 * a32) - a11 * (a02 * a33 - a03 * a32) + a31 * (a02 * a13 - a03 * a12))
        self[3]  = -(a01 * (a12 * a23 - a13 * a22) - a11 * (a02 * a23 - a03 * a22) + a21 * (a02 * a13 - a03 * a12))
        self[4]  = -(a10 * (a22 * a33 - a23 * a32) - a20 * (a12 * a33 - a13 * a32) + a30 * (a12 * a23 - a13 * a22))
        self[5]  =  (a00 * (a22 * a33 - a23 * a32) - a20 * (a02 * a33 - a03 * a32) + a30 * (a02 * a23 - a03 * a22))
        self[6]  = -(a00 * (a12 * a33 - a13 * a32) - a10 * (a02 * a33 - a03 * a32) + a30 * (a02 * a13 - a03 * a12))
        self[7]  =  (a00 * (a12 * a23 - a13 * a22) - a10 * (a02 * a23 - a03 * a22) + a20 * (a02 * a13 - a03 * a12))
        self[8]  =  (a10 * (a21 * a33 - a23 * a31) - a20 * (a11 * a33 - a13 * a31) + a30 * (a11 * a23 - a13 * a21))
        self[9]  = -(a00 * (a21 * a33 - a23 * a31) - a20 * (a01 * a33 - a03 * a31) + a30 * (a01 * a23 - a03 * a21))
        self[10] =  (a00 * (a11 * a33 - a13 * a31) - a10 * (a01 * a33 - a03 * a31) + a30 * (a01 * a13 - a03 * a11))
        self[11] = -(a00 * (a11 * a23 - a13 * a21) - a10 * (a01 * a23 - a03 * a21) + a20 * (a01 * a13 - a03 * a11))
        self[12] = -(a10 * (a21 * a32 - a22 * a31) - a20 * (a11 * a32 - a12 * a31) + a30 * (a11 * a22 - a12 * a21))
        self[13] =  (a00 * (a21 * a32 - a22 * a31) - a20 * (a01 * a32 - a02 * a31) + a30 * (a01 * a22 - a02 * a21))
        self[14] = -(a00 * (a11 * a32 - a12 * a31) - a10 * (a01 * a32 - a02 * a31) + a30 * (a01 * a12 - a02 * a11))
        self[15] =  (a00 * (a11 * a22 - a12 * a21) - a10 * (a01 * a22 - a02 * a21) + a20 * (a01 * a12 - a02 * a11))
        return self

    def determinant(a):
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

        return b00 * b11 - b01 * b10 + b02 * b09 + b03 * b08 - b04 * b07 + b05 * b06

    def multiply(self, a, b):
        a00 = a[0]; a01 = a[1]; a02 = a[2]; a03 = a[3]
        a10 = a[4]; a11 = a[5]; a12 = a[6]; a13 = a[7]
        a20 = a[8]; a21 = a[9]; a22 = a[10]; a23 = a[11]
        a30 = a[12]; a31 = a[13]; a32 = a[14]; a33 = a[15]

        b0 = b[0]; b1 = b[1]; b2 = b[2]; b3 = b[3];  
        self[0] = b0*a00 + b1*a10 + b2*a20 + b3*a30
        self[1] = b0*a01 + b1*a11 + b2*a21 + b3*a31
        self[2] = b0*a02 + b1*a12 + b2*a22 + b3*a32
        self[3] = b0*a03 + b1*a13 + b2*a23 + b3*a33

        b0 = b[4]; b1 = b[5]; b2 = b[6]; b3 = b[7]
        self[4] = b0*a00 + b1*a10 + b2*a20 + b3*a30
        self[5] = b0*a01 + b1*a11 + b2*a21 + b3*a31
        self[6] = b0*a02 + b1*a12 + b2*a22 + b3*a32
        self[7] = b0*a03 + b1*a13 + b2*a23 + b3*a33

        b0 = b[8]; b1 = b[9]; b2 = b[10]; b3 = b[11]
        self[8] = b0*a00 + b1*a10 + b2*a20 + b3*a30
        self[9] = b0*a01 + b1*a11 + b2*a21 + b3*a31
        self[10] = b0*a02 + b1*a12 + b2*a22 + b3*a32
        self[11] = b0*a03 + b1*a13 + b2*a23 + b3*a33

        b0 = b[12]; b1 = b[13]; b2 = b[14]; b3 = b[15]
        self[12] = b0*a00 + b1*a10 + b2*a20 + b3*a30
        self[13] = b0*a01 + b1*a11 + b2*a21 + b3*a31
        self[14] = b0*a02 + b1*a12 + b2*a22 + b3*a32
        self[15] = b0*a03 + b1*a13 + b2*a23 + b3*a33
        return self

    def translate(self, a, v):
        x = v[0]; y = v[1]; z = v[2]

        if a is self:
            self[12] = a[0] * x + a[4] * y + a[8] * z + a[12]
            self[13] = a[1] * x + a[5] * y + a[9] * z + a[13]
            self[14] = a[2] * x + a[6] * y + a[10] * z + a[14]
            self[15] = a[3] * x + a[7] * y + a[11] * z + a[15]
        else:
            a00 = a[0]; a01 = a[1]; a02 = a[2]; a03 = a[3]
            a10 = a[4]; a11 = a[5]; a12 = a[6]; a13 = a[7]
            a20 = a[8]; a21 = a[9]; a22 = a[10]; a23 = a[11]

            self[0] = a00; self[1] = a01; self[2] = a02; self[3] = a03
            self[4] = a10; self[5] = a11; self[6] = a12; self[7] = a13
            self[8] = a20; self[9] = a21; self[10] = a22; self[11] = a23

            self[12] = a00 * x + a10 * y + a20 * z + a[12]
            self[13] = a01 * x + a11 * y + a21 * z + a[13]
            self[14] = a02 * x + a12 * y + a22 * z + a[14]
            self[15] = a03 * x + a13 * y + a23 * z + a[15]
        return self

    def scale(self, a, v):
        x = v[0]; y = v[1]; z = v[2]

        self[0] = a[0] * x
        self[1] = a[1] * x
        self[2] = a[2] * x
        self[3] = a[3] * x
        self[4] = a[4] * y
        self[5] = a[5] * y
        self[6] = a[6] * y
        self[7] = a[7] * y
        self[8] = a[8] * z
        self[9] = a[9] * z
        self[10] = a[10] * z
        self[11] = a[11] * z
        self[12] = a[12]
        self[13] = a[13]
        self[14] = a[14]
        self[15] = a[15]
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

        a00 = a[0]; a01 = a[1]; a02 = a[2]; a03 = a[3]
        a10 = a[4]; a11 = a[5]; a12 = a[6]; a13 = a[7]
        a20 = a[8]; a21 = a[9]; a22 = a[10]; a23 = a[11]

        b00 = x * x * t + c; b01 = y * x * t + z * s; b02 = z * x * t - y * s
        b10 = x * y * t - z * s; b11 = y * y * t + c; b12 = z * y * t + x * s
        b20 = x * z * t + y * s; b21 = y * z * t - x * s; b22 = z * z * t + c

        self[0] = a00 * b00 + a10 * b01 + a20 * b02
        self[1] = a01 * b00 + a11 * b01 + a21 * b02
        self[2] = a02 * b00 + a12 * b01 + a22 * b02
        self[3] = a03 * b00 + a13 * b01 + a23 * b02
        self[4] = a00 * b10 + a10 * b11 + a20 * b12
        self[5] = a01 * b10 + a11 * b11 + a21 * b12
        self[6] = a02 * b10 + a12 * b11 + a22 * b12
        self[7] = a03 * b10 + a13 * b11 + a23 * b12
        self[8] = a00 * b20 + a10 * b21 + a20 * b22
        self[9] = a01 * b20 + a11 * b21 + a21 * b22
        self[10] = a02 * b20 + a12 * b21 + a22 * b22
        self[11] = a03 * b20 + a13 * b21 + a23 * b22

        if a is not self:
            self[12] = a[12]
            self[13] = a[13]
            self[14] = a[14]
            self[15] = a[15]
    
        return self

    def from_rotation_translation(self, q, v):
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
        self[1] = xy + wz
        self[2] = xz - wy
        self[3] = 0.0
        self[4] = xy - wz
        self[5] = 1.0 - (xx + zz)
        self[6] = yz + wx
        self[7] = 0.0
        self[8] = xz + wy
        self[9] = yz - wx
        self[10] = 1.0 - (xx + yy)
        self[11] = 0.0
        self[12] = v[0]
        self[13] = v[1]
        self[14] = v[2]
        self[15] = 1.0
        
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
        self[1] = xy + wz
        self[2] = xz - wy
        self[3] = 0.0

        self[4] = xy - wz
        self[5] = 1.0 - (xx + zz)
        self[6] = yz + wx
        self[7] = 0.0

        self[8] = xz + wy
        self[9] = yz - wx
        self[10] = 1.0 - (xx + yy)
        self[11] = 0.0

        self[12] = 0.0
        self[13] = 0.0
        self[14] = 0.0
        self[15] = 1.0

        return self

    def frustum(self, left, right, bottom, top, near, far):
        rl = 1.0 / (right - left)
        tb = 1.0 / (top - bottom)
        nf = 1.0 / (near - far)
        self[0] = (near * 2.0) * rl
        self[1] = 0.0
        self[2] = 0.0
        self[3] = 0.0
        self[4] = 0.0
        self[5] = (near * 2.0) * tb
        self[6] = 0.0
        self[7] = 0.0
        self[8] = (right + left) * rl
        self[9] = (top + bottom) * tb
        self[10] = (far + near) * nf
        self[11] = -1.0
        self[12] = 0.0
        self[13] = 0.0
        self[14] = (far * near * 2.0) * nf
        self[15] = 0.0
        return self

    def perspective(self, fovy, aspect, near, far):
        f = 1.0 / math.tan(fovy / 2.0)
        nf = 1.0 / (near - far)
        self[0] = f / aspect
        self[1] = 0.0
        self[2] = 0.0
        self[3] = 0.0
        self[4] = 0.0
        self[5] = f
        self[6] = 0.0
        self[7] = 0.0
        self[8] = 0.0
        self[9] = 0.0
        self[10] = (far + near) * nf
        self[11] = -1.0
        self[12] = 0.0
        self[13] = 0.0
        self[14] = (2.0 * far * near) * nf
        self[15] = 0.0
        return self

    def ortho(self, left, right, bottom, top, near, far):
        lr = 1.0 / (left - right)
        bt = 1.0 / (bottom - top)
        nf = 1.0 / (near - far)
        self[0] = -2.0 * lr
        self[1] = 0.0
        self[2] = 0.0
        self[3] = 0.0
        self[4] = 0.0
        self[5] = -2.0 * bt
        self[6] = 0.0
        self[7] = 0.0
        self[8] = 0.0
        self[9] = 0.0
        self[10] = 2.0 * nf
        self[11] = 0.0
        self[12] = (left + right) * lr
        self[13] = (top + bottom) * bt
        self[14] = (far + near) * nf
        self[15] = 1.0
        return self

    def look_at(self, eye, center, up):
        eyex = eye[0]
        eyey = eye[1]
        eyez = eye[2]
        upx = up[0]
        upy = up[1]
        upz = up[2]
        centerx = center[0]
        centery = center[1]
        centerz = center[2]

        if (math.abs(eyex - centerx) < GLMAT_EPSILON and
            math.abs(eyey - centery) < GLMAT_EPSILON and
            math.abs(eyez - centerz) < GLMAT_EPSILON):
            return self.identity()

        z0 = eyex - centerx
        z1 = eyey - centery
        z2 = eyez - centerz

        len = 1.0 / math.sqrt(z0 * z0 + z1 * z1 + z2 * z2)
        z0 *= len
        z1 *= len
        z2 *= len

        x0 = upy * z2 - upz * z1
        x1 = upz * z0 - upx * z2
        x2 = upx * z1 - upy * z0
        len = math.sqrt(x0 * x0 + x1 * x1 + x2 * x2)
        if len == 0.0:
            x0 = 0.0
            x1 = 0.0
            x2 = 0.0
        else:
            len = 1.0 / len
            x0 *= len
            x1 *= len
            x2 *= len

        y0 = z1 * x2 - z2 * x1
        y1 = z2 * x0 - z0 * x2
        y2 = z0 * x1 - z1 * x0

        len = math.sqrt(y0 * y0 + y1 * y1 + y2 * y2)
        if len == 0.0:
            y0 = 0.0
            y1 = 0.0
            y2 = 0.0
        else:
            len = 1.0 / len
            y0 *= len
            y1 *= len
            y2 *= len

        self[0] = x0
        self[1] = y0
        self[2] = z0
        self[3] = 0.0
        self[4] = x1
        self[5] = y1
        self[6] = z1
        self[7] = 0.0
        self[8] = x2
        self[9] = y2
        self[10] = z2
        self[11] = 0.0
        self[12] = -(x0 * eyex + x1 * eyey + x2 * eyez)
        self[13] = -(y0 * eyex + y1 * eyey + y2 * eyez)
        self[14] = -(z0 * eyex + z1 * eyey + z2 * eyez)
        self[15] = 1.0

        return self
