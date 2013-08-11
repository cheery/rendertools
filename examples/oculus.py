import pygame, time, sys, math
from pygame.locals import *
from rendertools.oculusrift import OculusRift
from rendertools.glmatrix import vec3, vec4, mat3, mat4, quat, radians
from rendertools import gl, hex2color, Image, Program, VertexFormat, VertexStream

display = OculusRift.openContext()

# look at grumpycat again.
image = Image.load('grumpycat.jpg')
grumpy = gl.createTexture()
gl.enable(gl.TEXTURE_2D)
gl.bindTexture(gl.TEXTURE_2D, grumpy)
gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, image.width, image.height, 0, image.format, image.type, image.data)
gl.texParameter(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR)
gl.texParameter(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR)
gl.bindTexture(gl.TEXTURE_2D, 0)

grumpy_gpu = Program.fromSource("""
    #version 120
    precision highp float;
VERTEX:
    attribute vec2 position;
    varying vec2 screen;
    uniform mat4 projection, inv_camera, modelview;
    void main() {
        screen = position;
        gl_Position = projection * inv_camera * modelview * vec4(position, 0.0, 1.0);
    }
FRAGMENT:
    varying vec2 screen;
    uniform sampler2D texture;
    void main() {
        gl_FragColor = texture2D(texture, screen);
    }
""")

data = (gl.gl_float*12)(
    -1.0, -1.0, +1.0, -1.0, +1.0, +1.0,
    -1.0, -1.0, +1.0, +1.0, -1.0, +1.0,
)
quad_vbo = gl.createBuffer()
gl.bindBuffer(gl.ARRAY_BUFFER, quad_vbo)
gl.bufferData(gl.ARRAY_BUFFER, gl.sizeof(data), data, gl.STATIC_DRAW)
gl.bindBuffer(gl.ARRAY_BUFFER, 0)
position2 = VertexFormat([
    ('position', 2, gl.FLOAT, gl.FALSE),
])

width, height = display.width, display.height

projection0 = display.perspective(-1, 0.1, 100.0)
projection1 = display.perspective(+1, 0.1, 100.0)
modelview = mat4()
modelview.translate(modelview, (0, 0, 0)).scale(modelview, (2,2,2))
camera = mat4()
camera.translate(camera, (0, 0, 1))
inv_camera = mat4()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False


    display.begin()

    gl.enable(gl.DEPTH_TEST)
    gl.enable(gl.TEXTURE_2D)
    gl.clearColor(0.2, 0.0, 0.4, 1.0)
    gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT)

    gpu = grumpy_gpu
    gl.useProgram(gpu)
    width  = display.width/2
    height = display.height

    gl.viewport(0,0,width,height)
    gl.bindBuffer(gl.ARRAY_BUFFER, quad_vbo)
    gl.bindTexture(gl.TEXTURE_2D, grumpy)
    gl.uniformMatrix4fv(gpu.loc('projection'), 1, gl.FALSE, gl.floats(projection0))
    gl.uniformMatrix4fv(gpu.loc('modelview'),  1, gl.FALSE, gl.floats(modelview))
    gl.uniformMatrix4fv(gpu.loc('inv_camera'), 1, gl.FALSE, gl.floats(display.shiftCameraInv(inv_camera, camera, -1)))
    position2.enable(gpu)
    gl.drawArrays(gl.TRIANGLES, 0, 6)
    position2.disable(gpu)
    gl.bindTexture(gl.TEXTURE_2D, 0)
    gl.bindBuffer(gl.ARRAY_BUFFER, 0)

    gl.viewport(width,0,width,height)
    gl.bindBuffer(gl.ARRAY_BUFFER, quad_vbo)
    gl.bindTexture(gl.TEXTURE_2D, grumpy)
    gl.uniformMatrix4fv(gpu.loc('projection'), 1, gl.FALSE, gl.floats(projection1))
    gl.uniformMatrix4fv(gpu.loc('modelview'),  1, gl.FALSE, gl.floats(modelview))
    gl.uniformMatrix4fv(gpu.loc('inv_camera'), 1, gl.FALSE, gl.floats(display.shiftCameraInv(inv_camera, camera, +1)))
    position2.enable(gpu)
    gl.drawArrays(gl.TRIANGLES, 0, 6)
    position2.disable(gpu)
    gl.bindTexture(gl.TEXTURE_2D, 0)
    gl.bindBuffer(gl.ARRAY_BUFFER, 0)

    display.end()

#    gl.bindFramebuffer(gl.FRAMEBUFFER, 0)
#
#
#    w, h = info.HResolution/2, info.VResolution
#    aspect = info.HResolution / (2.0 * info.VResolution)
#    offset = 1.0 - 2.0*info.LensSeparationDistance/info.HScreenSize
#    scale  = aspect * distort(info.DistortionK, 1.0 + offset)
#
#    gpu = postprocess_gpu
#    gl.disable(gl.DEPTH_TEST)
#    gl.enable(gl.TEXTURE_2D)
#    gl.useProgram(gpu)
#    gl.uniform4fv(gpu.loc('distortion_k'), 1, info.DistortionK)
#    gl.uniform2f(gpu.loc('scalein'),  1.0,         1.0 / aspect)
#    gl.uniform2f(gpu.loc('scaleout'), 1.0 / scale, aspect / scale)
#    gl.bindBuffer(gl.ARRAY_BUFFER, quad_vbo)
#    gl.bindTexture(gl.TEXTURE_2D, color)
#    position2.enable(gpu)
#    gl.viewport(0, 0, w, h)
#    gl.uniform2f(gpu.loc('center'), 0.25, 0.5)
#    gl.uniform2f(gpu.loc('offset'), +offset, 0.0)
#    gl.drawArrays(gl.TRIANGLES, 0, 6)
#    gl.viewport(w, 0, w, h)
#    gl.uniform2f(gpu.loc('center'), 0.75, 0.5)
#    gl.uniform2f(gpu.loc('offset'), -offset, 0.0)
#    gl.drawArrays(gl.TRIANGLES, 0, 6)
#    position2.disable(gpu)
#    gl.bindTexture(gl.TEXTURE_2D, 0)
#    gl.bindBuffer(gl.ARRAY_BUFFER, 0)
#    gl.useProgram(0)
#
#    pygame.display.flip()
