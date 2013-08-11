import pygame, time, sys, math
from pygame.locals import *

from rendertools.glmatrix import vec3, vec4, mat3, mat4, quat, radians

was = time.time()
from rendertools import gl, hex2color, Image, Program, VertexFormat, VertexStream
now = time.time()
print 'gl loading took %i ms' % ((now-was) * 1000.0)

resolution = 640, 480
flags = OPENGL | DOUBLEBUF | HWSURFACE | NOFRAME

pygame.display.set_mode(resolution, flags)

if gl.getCurrentContext() == 0:
    raise Exception("OpenGL missing")

program = Program.fromSource("""
VERTEX:
    attribute vec3 position;
    uniform vec3 offset;
    uniform vec3 scale;
    varying vec3 i_position;
    void main() {
        i_position = position;
        gl_Position = vec4((position - offset) * scale, 1.0);
    }
FRAGMENT:
    uniform sampler2D texture;
    uniform vec4 color;
    varying vec3 i_position;
    void main() {
        gl_FragColor = color * texture2D(texture, i_position.xy);
    }
""")

pointstream = VertexStream(VertexFormat([
    ('position', 3, gl.FLOAT, gl.FALSE),
]))
gl.enable(gl.VERTEX_PROGRAM_POINT_SIZE)
gl.enable(gl.POINT_SPRITE)
#gl.enable(gl.POINT_SMOOTH)
pointgpu = Program.fromSource("""
    #version 120
VERTEX:
    float rand(vec2 co){
        return fract(sin(dot(co.xy ,vec2(12.9898,78.233))) * 43758.5453);
    }
    attribute vec3 position;
    void main() {
        gl_PointSize = rand(position.xy) * 12.0;
        gl_Position = vec4(position, 1.0);
    }
FRAGMENT:
    void main() {
        float mag = length(gl_PointCoord.xy - 0.5) * 2.0;
        float opacity = (1.0 - mag)*(1.0 - mag);
        if (mag > 1.0) discard;
        gl_FragColor = vec4(1.0, mag, 0.0, 1.0) * opacity;
    }
""")

data = (gl.gl_float*18)(
    0.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 1.0, 0.0,
    0.0, 0.0, 0.0,
    1.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
)
size = gl.sizeof(data)

# CODE TO CREATE THE BUFFER
vbo = gl.createBuffer()
gl.bindBuffer(gl.ARRAY_BUFFER, vbo)
gl.bufferData(gl.ARRAY_BUFFER, size, data, gl.STATIC_DRAW)
gl.bindBuffer(gl.ARRAY_BUFFER, 0)

# CODE TO INSERT THE IMAGE
image = Image.load('grumpycat.jpg')
texture = gl.createTexture()
gl.enable(gl.TEXTURE_2D)
gl.bindTexture(gl.TEXTURE_2D, texture)
gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, image.width, image.height, 0, image.format, image.type, image.data)
gl.texParameter(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR)
gl.texParameter(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR)

gl.viewport(0, 0, *resolution)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False

#    was = time.time()

    gl.useProgram(program)
    gl.clearColor(0.2, 0.0, 0.4, 1.0)
    gl.clear(gl.COLOR_BUFFER_BIT)

    u = program.loc('color')
    if u >= 0:
        gl.uniform4f(u, 0.4, 0.4, 0.0, 1.0)

    u = program.loc('scale')
    if u >= 0:
        gl.uniform3f(u, 1.0, 1.0*image.height/image.width, 0.0)

    gl.bindBuffer(gl.ARRAY_BUFFER, vbo)

    a = program.attribLoc('position')
    if a >= 0:
        gl.enableVertexAttribArray(a)
        gl.vertexAttribPointer(a, 3, gl.FLOAT, gl.FALSE, 0, 0)

    now = time.time()
    offsets = [
        (math.cos(now*5)*0.5+0.5, math.sin(now*2)*0.5+0.5),
        (math.cos(now)*0.5+0.5, math.sin(now)*0.5+0.5),
        (0.5, 0.5),
    ]
    for x,y in offsets:
        u = program.loc('offset')
        if u >= 0:
            gl.uniform3f(u, x, y, 0.0)
        gl.drawArrays(gl.TRIANGLES, 0, len(data))

    if a >= 0:
        gl.disableVertexAttribArray(a)


    gl.enable(gl.BLEND)
    gl.blendFunc(gl.ONE, gl.ONE)
    gl.useProgram(pointgpu)
    vertex = pointstream.vertex
    emit   = pointstream.emit

    points = [
        (-0.9, -0.9),
        (-0.8, -0.8),
        (-0.7, -0.7),
        (-0.6, -0.6),
        (-0.5, -0.5),
        (-0.4, -0.4),
        (-0.3, -0.3),
        (-0.2, -0.2),
        (-0.1, -0.1),
        (0.0, 0.0),
        (0.1, 0.1),
        (0.2, 0.2),
        (0.3, 0.3),
        (0.4, 0.4),
        (0.5, 0.5),
        (0.6, 0.6),
        (0.7, 0.7),
        (0.8, 0.8),
        (0.9, 0.9),
    ]
    for x,y in points:
        vertex.position[:] = math.sin(now*x)*x, math.cos(now*y)*y, 0.0
        emit()
    pointstream.draw(pointgpu, gl.POINTS)
    gl.disable(gl.BLEND)

#    now = time.time()
#    delta = was - now
#    print '%i ms' % (delta * 1000.0)

    pygame.display.flip()
    

#    prev = time.time()
#    now = time.time()
#    print '%i FPS' % (1.0 / (now - prev))
#    prev = now
