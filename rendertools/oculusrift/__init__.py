import pygame, ovr, os, math
from pygame.locals import *
from rendertools.glmatrix import vec3, vec4, mat3, mat4, quat, radians
from rendertools import gl, Program, VertexFormat, VertexStream

postprocess_source = """
    #version 120
    precision highp float;
VERTEX:
    attribute vec2 position;
    varying vec2 screen;
    void main() {
        screen = position;
        gl_Position = vec4(position, 0.0, 1.0);
    }
FRAGMENT:
    varying vec2 screen;
    uniform sampler2D texture;
    uniform vec4 distortion_k;
    uniform vec4 chromab;
    uniform vec2 center;
    uniform vec2 offset;
    uniform vec2 scalein;
    uniform vec2 scaleout;
    void main() {
        vec2 theta = (screen - offset) * scalein;
        float rsq = theta.x * theta.x + theta.y * theta.y;
        vec2 theta1 = theta * (
            distortion_k.x +
            distortion_k.y * rsq +
            distortion_k.z * rsq * rsq +
            distortion_k.w * rsq * rsq * rsq
        );
        //return scaleout * r + offset;

        // chromatic aberration
        vec2 thetablue = theta1 * (chromab.z + chromab.w * rsq);
        vec2 tblue = offset + scaleout * thetablue;

        // blue gets scaled out furthest, so check against them whether we are out of range.
        vec2 d = clamp(tblue, vec2(-1.0, -1.0), vec2(1.0, 1.0)) - tblue;
        if ((d.x != 0) || (d.y != 0)) discard;

        vec2 tgreen = offset + scaleout * theta1;
        
        vec2 thetared = theta1 * (chromab.x + chromab.y * rsq);
        vec2 tred = offset + scaleout * thetared;

        gl_FragColor = vec4(
            texture2D(texture, tred*vec2(0.25, 0.5) + center).r,
            texture2D(texture, tgreen*vec2(0.25, 0.5) + center).g,
            texture2D(texture, tblue*vec2(0.25, 0.5) + center).b,
            1.0
        );
    }
"""

def loadRift():
    out = ovr.OVR_HMDInfo()
    if ovr.init() != 0 and ovr.queryHMD(gl.byref(out)) != 0:
        return out

def peekRift():
    yaw = gl.gl_float()
    pitch = gl.gl_float()
    roll = gl.gl_float()
    if ovr.peek(gl.byref(yaw), gl.byref(pitch), gl.byref(roll)) == 0:
        raise Exception("ovr.peek failed")
    return yaw.value, pitch.value, roll.value

def distort((k0, k1, k2, k3), v):
    rsq = v*v
    return v * (k0 + k1*rsq + k2*rsq*rsq + k3*rsq*rsq*rsq)

class ScreenQuad(object):
    def __init__(self):
        data = (gl.gl_float*12)(
            -1.0, -1.0, +1.0, -1.0, +1.0, +1.0,
            -1.0, -1.0, +1.0, +1.0, -1.0, +1.0,
        )
        self.vbo = gl.createBuffer()
        gl.bindBuffer(gl.ARRAY_BUFFER, self.vbo)
        gl.bufferData(gl.ARRAY_BUFFER, gl.sizeof(data), data, gl.STATIC_DRAW)
        gl.bindBuffer(gl.ARRAY_BUFFER, 0)
        self.vertexformat = VertexFormat([
            ('position', 2, gl.FLOAT, gl.FALSE),
        ])

class Frame(object):
    def __init__(self, width, height):
        self.width  = width
        self.height = height
        self.color = gl.createTexture()
        gl.bindTexture(gl.TEXTURE_2D, self.color)
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, width, height, 0, gl.RGBA, gl.UNSIGNED_BYTE, None)
        gl.texParameter(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR)
        gl.texParameter(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR)
        gl.bindTexture(gl.TEXTURE_2D, 0)

        self.depthbuffer = gl.createRenderbuffer()
        gl.bindRenderbuffer(gl.RENDERBUFFER, self.depthbuffer)
        gl.renderbufferStorage(gl.RENDERBUFFER, gl.DEPTH_COMPONENT, width, height)
        gl.bindRenderbuffer(gl.RENDERBUFFER, 0)

        self.framebuffer = gl.createFramebuffer()
        gl.bindFramebuffer(gl.FRAMEBUFFER, self.framebuffer)
        gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, self.color, 0)
        gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.RENDERBUFFER, self.depthbuffer)
        gl.bindFramebuffer(gl.FRAMEBUFFER, 0)

    def postprocess(self, info, gpu, quad):
        w, h = info.HResolution/2, info.VResolution
        aspect = info.HResolution / (2.0 * info.VResolution)
        offset = 1.0 - 2.0*info.LensSeparationDistance/info.HScreenSize
        scale  = aspect * distort(info.DistortionK, 1.0 + offset)
        gl.disable(gl.DEPTH_TEST)
        gl.enable(gl.TEXTURE_2D)
        gl.useProgram(gpu)
        gl.uniform4fv(gpu.loc('distortion_k'), 1, info.DistortionK)
        gl.uniform4fv(gpu.loc('chromab'), 1, info.ChromaAbCorrection)
        gl.uniform2f(gpu.loc('scalein'),  1.0,         1.0 / aspect)
        gl.uniform2f(gpu.loc('scaleout'), 1.0 / scale, aspect / scale)
        gl.bindBuffer(gl.ARRAY_BUFFER, quad.vbo)
        gl.bindTexture(gl.TEXTURE_2D, self.color)
        quad.vertexformat.enable(gpu)
        gl.viewport(0, 0, w, h)
        gl.uniform2f(gpu.loc('center'), 0.25, 0.5)
        gl.uniform2f(gpu.loc('offset'), +offset, 0.0)
        gl.drawArrays(gl.TRIANGLES, 0, 6)
        gl.viewport(w, 0, w, h)
        gl.uniform2f(gpu.loc('center'), 0.75, 0.5)
        gl.uniform2f(gpu.loc('offset'), -offset, 0.0)
        gl.drawArrays(gl.TRIANGLES, 0, 6)
        quad.vertexformat.disable(gpu)
        gl.bindTexture(gl.TEXTURE_2D, 0)
        gl.bindBuffer(gl.ARRAY_BUFFER, 0)
        gl.useProgram(0)

class OculusRift(object):
    def __init__(self, info, gpu, quad, frame):
        self.info = info
        self.gpu  = gpu
        self.quad = quad
        self.frame  = frame
        self.width  = frame.width
        self.height = frame.height

    @classmethod
    def openContext(cls):
        info = loadRift()
        if info is None:
            raise Exception("Oculus Rift missing")
        resolution = info.HResolution, info.VResolution
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (info.DesktopX, info.DesktopY)
        flags = OPENGL | DOUBLEBUF | HWSURFACE | NOFRAME
        pygame.display.set_mode(resolution, flags)
        if gl.getCurrentContext() == 0:
            raise Exception("OpenGL missing")
        gpu = Program.fromSource(postprocess_source)
        quad = ScreenQuad()
        frame = Frame(int(info.HResolution*1.25), int(info.VResolution*1.25))
        return cls(info, gpu, quad, frame)

    def perspective(self, eye, near, far):
        info = self.info
        out = mat4()
        h_meters = info.HScreenSize/4.0 - info.LensSeparationDistance/2.0
        h = (4.0*h_meters) / info.HScreenSize
        h = (info.HScreenSize - info.LensSeparationDistance*2.0) / info.HScreenSize
        out[12] = eye * -h

        w, h = info.HResolution/2, info.VResolution
        aspect = info.HResolution / (2.0 * info.VResolution)
        offset = 1.0 - 2.0*info.LensSeparationDistance/info.HScreenSize
        scale  = aspect * distort(info.DistortionK, 1.0 + offset)
        fovy = 2.0 * math.atan(scale * info.VScreenSize / (2.0 * info.EyeToScreenDistance))
        persp = mat4().perspective(fovy, aspect, near, far)

        return out.multiply(out, persp)

    def shiftCameraInv(self, tmp, camera, eye):
        yaw, pitch, roll = peekRift()
        camera = tmp.copy(camera)
        camera.rotate(camera, yaw,   (0,1,0))
        camera.rotate(camera, pitch, (1,0,0))
        camera.rotate(camera, roll,  (0,0,1))
        camera.translate(camera, (eye * -self.info.InterpupillaryDistance/2.0, 0.0, 0.0))
        return tmp.invert(camera)

    def begin(self):
        gl.bindFramebuffer(gl.FRAMEBUFFER, self.frame.framebuffer)

    def end(self):
        gl.bindFramebuffer(gl.FRAMEBUFFER, 0)
        self.frame.postprocess(self.info, self.gpu, self.quad)
        pygame.display.flip()

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, type, value, callback):
        return self.end()
